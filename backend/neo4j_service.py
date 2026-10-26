"""
Mandate Radar Neo4j Knowledge Graph Service
Handles live Neo4j Aura connection, graph synchronization, Cypher queries,
and includes an embedded graph engine so the entire system works instantly.
"""

import os
from typing import Dict, List, Any, Optional
import neo4j
from reference_data import REFERENCE_MERCHANTS, PARENT_COMPANIES, PAYMENT_MECHANISMS, ESCALATION_CHAIN

class Neo4jKnowledgeGraph:
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        self.uri = uri or os.getenv("NEO4J_URI", "")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "")
        self.driver: Optional[neo4j.Driver] = None
        self.is_connected = False
        self.connection_error = None

        # Embedded in-memory graph fallback
        self.nodes = []
        self.edges = []
        self._build_embedded_reference_graph()

        # Try connecting if uri is supplied
        if self.uri and self.password:
            self.connect()

    def connect(self, uri: str = None, user: str = None, password: str = None):
        if uri: self.uri = uri
        if user: self.user = user
        if password: self.password = password

        if not self.uri or not self.password:
            self.is_connected = False
            self.connection_error = "Neo4j URI or Password not provided. Operating in Embedded Graph Mode."
            return False, self.connection_error

        try:
            self.driver = neo4j.GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                max_connection_lifetime=300
            )
            self.driver.verify_connectivity()
            self.is_connected = True
            self.connection_error = None
            return True, "Successfully connected to Neo4j instance!"
        except Exception as e:
            self.is_connected = False
            self.connection_error = str(e)
            return False, f"Neo4j Connection Failed: {str(e)}"

    def close(self):
        if self.driver:
            self.driver.close()

    def _build_embedded_reference_graph(self):
        """Constructs the base in-memory graph of reference nodes and relationships."""
        self.nodes = []
        self.edges = []
        edge_id = 1

        # 1. Parents
        for pid, pdata in PARENT_COMPANIES.items():
            self.nodes.append({
                "id": f"parent_{pid}",
                "label": "Parent",
                "name": pdata["name"],
                "group": "parent",
                "color": "#6366F1", # Indigo
                "val": 28,
                "properties": pdata
            })

        # 2. Mechanisms
        for mcode, mdata in PAYMENT_MECHANISMS.items():
            self.nodes.append({
                "id": f"mech_{mcode}",
                "label": "Mechanism",
                "name": mdata["name"],
                "group": "mechanism",
                "color": "#EC4899", # Pink
                "val": 22,
                "properties": mdata
            })

        # 3. Escalation Steps
        for esc in ESCALATION_CHAIN:
            self.nodes.append({
                "id": f"esc_tier_{esc['tier']}",
                "label": "EscalationStep",
                "name": f"Tier {esc['tier']}: {esc['name']}",
                "group": "escalation",
                "color": "#EF4444", # Red
                "val": 18,
                "properties": esc
            })

        # 4. Merchants & Edges
        for m in REFERENCE_MERCHANTS:
            m_node_id = f"merch_{m['id']}"
            self.nodes.append({
                "id": m_node_id,
                "label": "Merchant",
                "name": m["name"],
                "group": "merchant",
                "color": "#10B981", # Emerald
                "val": 20,
                "properties": {
                    "id": m["id"],
                    "name": m["name"],
                    "category": m["category"],
                    "website": m.get("official_website", ""),
                    "default_amount": m.get("default_amount", 0.0),
                    "pitfall": m.get("cancellation_pitfall", "")
                }
            })

            # Edge to Parent: (Merchant)-[:OWNED_BY]->(Parent)
            if m.get("parent_id") and f"parent_{m['parent_id']}" in [n["id"] for n in self.nodes]:
                self.edges.append({
                    "id": f"e_{edge_id}",
                    "source": m_node_id,
                    "target": f"parent_{m['parent_id']}",
                    "type": "OWNED_BY",
                    "label": "OWNED_BY",
                    "color": "#6366F1"
                })
                edge_id += 1

            # Edge to Default Mechanism: (Merchant)-[:BILLED_VIA]->(Mechanism)
            mech = m.get("default_mechanism", "CARD_SI")
            if f"mech_{mech}" in [n["id"] for n in self.nodes]:
                self.edges.append({
                    "id": f"e_{edge_id}",
                    "source": m_node_id,
                    "target": f"mech_{mech}",
                    "type": "BILLED_VIA",
                    "label": "BILLED_VIA",
                    "color": "#EC4899"
                })
                edge_id += 1

            # Descriptors: (Descriptor)-[:RESOLVES_TO]->(Merchant)
            for pat in m.get("descriptors", [])[:2]: # include top 2 representative patterns
                d_id = f"desc_{hash(pat) % 10000000}"
                self.nodes.append({
                    "id": d_id,
                    "label": "Descriptor",
                    "name": pat.replace(r"\s+", " ").replace(r"\d+", "###"),
                    "group": "descriptor",
                    "color": "#8B5CF6", # Purple
                    "val": 12,
                    "properties": {"pattern": pat}
                })
                self.edges.append({
                    "id": f"e_{edge_id}",
                    "source": d_id,
                    "target": m_node_id,
                    "type": "RESOLVES_TO",
                    "label": "RESOLVES_TO",
                    "color": "#8B5CF6"
                })
                edge_id += 1

    def sync_statement_mandates(self, person_name: str, mandates: List[Dict[str, Any]]):
        """
        Injects the user's detected mandates and charges into the graph:
        (Person)-[:HAS_MANDATE]->(Mandate)-[:FOR]->(Merchant)
        (Mandate)-[:VIA_MECHANISM]->(Mechanism)
        """
        # Add Person node
        person_id = "user_primary"
        # Remove old statement nodes if re-analyzing
        self.nodes = [n for n in self.nodes if n["group"] not in ["person", "mandate", "charge"]]
        self.edges = [e for e in self.edges if e["type"] not in ["HAS_MANDATE", "FOR", "VIA_MECHANISM", "HAD_CHARGE"]]

        self.nodes.append({
            "id": person_id,
            "label": "Person",
            "name": person_name,
            "group": "person",
            "color": "#F59E0B", # Amber
            "val": 32,
            "properties": {"name": person_name, "account_type": "Primary Account Holder"}
        })

        edge_counter = len(self.edges) + 100

        for mand in mandates:
            mand_node_id = f"mand_{mand['id']}"
            flag_color = {
                "PRICE_HIKE": "#F97316", # Orange
                "TRIAL_CONVERTED": "#EF4444", # Red
                "UNUSED_ZOMBIE": "#DC2626", # Deep Red
                "HEALTHY": "#10B981" # Green
            }.get(mand["flag"], "#3B82F6")

            self.nodes.append({
                "id": mand_node_id,
                "label": "Mandate",
                "name": f"₹{mand['latest_amount']:.0f} / {mand['cadence'][0]}",
                "group": "mandate",
                "color": flag_color,
                "val": 22,
                "properties": {
                    "cadence": mand["cadence"],
                    "amount": mand["latest_amount"],
                    "annual_committed": mand["annual_committed_cost"],
                    "flag": mand["flag"],
                    "flag_reason": mand["flag_reason"],
                    "descriptor": mand["descriptor"]
                }
            })

            # (Person)-[:HAS_MANDATE]->(Mandate)
            self.edges.append({
                "id": f"e_{edge_counter}",
                "source": person_id,
                "target": mand_node_id,
                "type": "HAS_MANDATE",
                "label": "HAS_MANDATE",
                "color": "#F59E0B"
            })
            edge_counter += 1

            # (Mandate)-[:FOR]->(Merchant)
            m_id = f"merch_{mand.get('merchant_id')}"
            if m_id in [n["id"] for n in self.nodes]:
                self.edges.append({
                    "id": f"e_{edge_counter}",
                    "source": mand_node_id,
                    "target": m_id,
                    "type": "FOR",
                    "label": "FOR",
                    "color": "#10B981"
                })
                edge_counter += 1

            # (Mandate)-[:VIA_MECHANISM]->(Mechanism)
            mech_id = f"mech_{mand.get('mechanism')}"
            if mech_id in [n["id"] for n in self.nodes]:
                self.edges.append({
                    "id": f"e_{edge_counter}",
                    "source": mand_node_id,
                    "target": mech_id,
                    "type": "VIA_MECHANISM",
                    "label": "VIA_MECHANISM",
                    "color": "#EC4899"
                })
                edge_counter += 1

    def run_cypher_query(self, cypher: str) -> Dict[str, Any]:
        """
        Executes a Cypher query on live Neo4j if connected,
        otherwise interprets preset queries against embedded graph.
        """
        if self.is_connected and self.driver:
            try:
                with self.driver.session() as session:
                    result = session.run(cypher)
                    records = [record.data() for record in result]
                    return {
                        "mode": "NEO4J_AURA_LIVE",
                        "status": "SUCCESS",
                        "cypher": cypher,
                        "count": len(records),
                        "data": records
                    }
            except Exception as e:
                return {
                    "mode": "NEO4J_AURA_LIVE",
                    "status": "ERROR",
                    "error": str(e),
                    "cypher": cypher,
                    "data": []
                }

        # Embedded Cypher emulation
        cypher_upper = cypher.upper()

        # 1. Multi-merchant parent footprint query
        if "OWNED_BY" in cypher_upper or "PARENT" in cypher_upper:
            parent_groups = {}
            for e in self.edges:
                if e["type"] == "OWNED_BY":
                    m_node = next((n for n in self.nodes if n["id"] == e["source"]), None)
                    p_node = next((n for n in self.nodes if n["id"] == e["target"]), None)
                    if m_node and p_node:
                        p_name = p_node["name"]
                        if p_name not in parent_groups:
                            parent_groups[p_name] = {"parent": p_name, "merchants": [], "total_subs": 0}
                        parent_groups[p_name]["merchants"].append(m_node["name"])
                        parent_groups[p_name]["total_subs"] += 1
            return {
                "mode": "EMBEDDED_GRAPH_ENGINE",
                "status": "SUCCESS",
                "cypher": cypher,
                "count": len(parent_groups),
                "data": list(parent_groups.values())
            }

        # 2. Cancellation route by mechanism query
        if "MECHANISM" in cypher_upper or "BILLED_VIA" in cypher_upper or "CANCELLED_BY" in cypher_upper:
            mech_routes = []
            for m in REFERENCE_MERCHANTS:
                mech_code = m.get("default_mechanism", "CARD_SI")
                mech_info = PAYMENT_MECHANISMS.get(mech_code, PAYMENT_MECHANISMS["CARD_SI"])
                mech_routes.append({
                    "merchant": m["name"],
                    "mechanism": mech_info["name"],
                    "turnaround": mech_info["turnaround_time"],
                    "primary_cancellation_step": mech_info["cancellation_steps"][0]
                })
            return {
                "mode": "EMBEDDED_GRAPH_ENGINE",
                "status": "SUCCESS",
                "cypher": cypher,
                "count": len(mech_routes),
                "data": mech_routes
            }

        # 3. High risk flags or price hike query
        if "FLAG" in cypher_upper or "PRICE_HIKE" in cypher_upper or "MANDATE" in cypher_upper:
            flagged = []
            for n in self.nodes:
                if n["label"] == "Mandate":
                    props = n.get("properties", {})
                    flagged.append({
                        "mandate_id": n["id"],
                        "amount": props.get("amount"),
                        "cadence": props.get("cadence"),
                        "annual_cost": props.get("annual_committed"),
                        "flag": props.get("flag"),
                        "flag_reason": props.get("flag_reason")
                    })
            return {
                "mode": "EMBEDDED_GRAPH_ENGINE",
                "status": "SUCCESS",
                "cypher": cypher,
                "count": len(flagged),
                "data": flagged
            }

        # Default fallback: return all nodes summary
        counts = {}
        for n in self.nodes:
            lbl = n.get("label", "Unknown")
            counts[lbl] = counts.get(lbl, 0) + 1
        return {
            "mode": "EMBEDDED_GRAPH_ENGINE",
            "status": "SUCCESS",
            "cypher": cypher,
            "count": len(self.nodes),
            "data": [{"node_label": k, "count": v} for k, v in counts.items()]
        }

    def generate_cypher_seed_script(self) -> str:
        """
        Generates full declarative Cypher DDL & Seed Script (.cql)
        ready to load into Neo4j Aura or Neo4j Desktop.
        """
        lines = [
            "// =================================================================",
            "// MANDATE RADAR: REFERENCE KNOWLEDGE GRAPH SEED SCRIPT (CYPHER)",
            "// Track: Neo4j (Best Use of Neo4j)",
            "// Theme: Fintech - The Auto Debits Nobody Can Find",
            "// =================================================================",
            "",
            "// 1. Constraints & Unique Indexes",
            "CREATE CONSTRAINT unique_merchant_id IF NOT EXISTS FOR (m:Merchant) REQUIRE m.id IS UNIQUE;",
            "CREATE CONSTRAINT unique_parent_id IF NOT EXISTS FOR (p:Parent) REQUIRE p.id IS UNIQUE;",
            "CREATE CONSTRAINT unique_mechanism_code IF NOT EXISTS FOR (mech:Mechanism) REQUIRE mech.code IS UNIQUE;",
            "CREATE CONSTRAINT unique_mandate_id IF NOT EXISTS FOR (mand:Mandate) REQUIRE mand.id IS UNIQUE;",
            "",
            "// 2. Parent Conglomerates",
        ]

        for pid, pdata in PARENT_COMPANIES.items():
            lines.append(
                f"MERGE (p:Parent {{id: '{pid}'}}) "
                f"ON CREATE SET p.name = '{pdata['name']}', p.ticker = '{pdata['ticker']}', "
                f"p.country = '{pdata['country']}', p.headquarters = '{pdata['headquarters']}';"
            )

        lines.append("")
        lines.append("// 3. Payment Mechanisms & Legal Rails")
        for mcode, mdata in PAYMENT_MECHANISMS.items():
            lines.append(
                f"MERGE (mech:Mechanism {{code: '{mcode}'}}) "
                f"ON CREATE SET mech.name = '{mdata['name']}', mech.authority = '{mdata['authority']}', "
                f"mech.turnaround = '{mdata['turnaround_time']}';"
            )

        lines.append("")
        lines.append("// 4. Merchants, Parent Hierarchy & Descriptors")
        for m in REFERENCE_MERCHANTS:
            mid = m["id"]
            mname = m["name"].replace("'", "\\'")
            cat = m["category"].replace("'", "\\'")
            amt = m.get("default_amount", 0.0)
            pid = m.get("parent_id")
            mech = m.get("default_mechanism", "CARD_SI")

            lines.append(
                f"MERGE (m:Merchant {{id: '{mid}'}}) "
                f"ON CREATE SET m.name = '{mname}', m.category = '{cat}', m.default_amount = {amt};"
            )

            if pid:
                lines.append(f"MATCH (m:Merchant {{id: '{mid}'}}), (p:Parent {{id: '{pid}'}}) MERGE (m)-[:OWNED_BY]->(p);")
            if mech:
                lines.append(f"MATCH (m:Merchant {{id: '{mid}'}}), (mech:Mechanism {{code: '{mech}'}}) MERGE (m)-[:BILLED_VIA]->(mech);")

            for pat in m.get("descriptors", [])[:2]:
                escaped_pat = pat.replace("\\", "\\\\").replace("'", "\\'")
                desc_key = f"desc_{abs(hash(pat)) % 1000000}"
                lines.append(
                    f"MERGE (d:Descriptor {{pattern: '{escaped_pat}'}}) "
                    f"MERGE (m:Merchant {{id: '{mid}'}}) "
                    f"MERGE (d)-[:RESOLVES_TO]->(m);"
                )

        lines.append("")
        lines.append("// 5. Verification Query: Inspect Parent Footprint & Multi-Subscription Traversal")
        lines.append("MATCH (p:Parent)<-[:OWNED_BY]-(m:Merchant)-[:BILLED_VIA]->(mech:Mechanism)")
        lines.append("RETURN p.name AS Parent, collect(DISTINCT m.name) AS Merchants, collect(DISTINCT mech.name) AS Mechanisms;")

        return "\n".join(lines)

    def get_graph_visualization_data(self, filter_mode: str = "portfolio") -> Dict[str, Any]:
        """
        Returns node/link payload for interactive Graph Visualizer.
        Filters by 'portfolio' (default, user's active mandates), 'alphabet', 'amazon',
        'streaming', or 'all' to prevent cluttered 270-node hairballs.
        """
        if filter_mode == "portfolio":
            # 1. Start with Person and Mandate nodes
            person_id = "user_primary"
            portfolio_mandate_ids = {n["id"] for n in self.nodes if n["group"] == "mandate"}
            active_ids = {person_id}.union(portfolio_mandate_ids)

            # 2. Find merchants and rails linked directly to user mandates
            merchant_ids = set()
            rail_ids = set()
            mandate_edges = []

            for e in self.edges:
                if e["source"] in portfolio_mandate_ids or e["target"] in portfolio_mandate_ids or e["source"] == person_id:
                    mandate_edges.append(e)
                    active_ids.add(e["source"])
                    active_ids.add(e["target"])
                    if e["type"] == "FOR":
                        merchant_ids.add(e["target"])
                    if e["type"] == "VIA_MECHANISM":
                        rail_ids.add(e["target"])

            # 3. From ONLY the active merchants, find their parents (OUTGOING ONLY, so unrelated merchants aren't pulled in)
            parent_edges = []
            for e in self.edges:
                if e["source"] in merchant_ids and e["type"] == "OWNED_BY":
                    parent_edges.append(e)
                    active_ids.add(e["target"])

            all_portfolio_edges = mandate_edges + parent_edges
            filtered_nodes = [n for n in self.nodes if n["id"] in active_ids]
            filtered_edges = all_portfolio_edges

        elif filter_mode == "alphabet":
            target_parent = "parent_alphabet"
            sub_ids = {target_parent}
            for e in self.edges:
                if e["target"] == target_parent or e["source"] == target_parent:
                    sub_ids.add(e["source"])
                    sub_ids.add(e["target"])
            for e in self.edges:
                if e["source"] in sub_ids or e["target"] in sub_ids:
                    sub_ids.add(e["source"])
                    sub_ids.add(e["target"])
            filtered_nodes = [n for n in self.nodes if n["id"] in sub_ids]
            filtered_edges = [e for e in self.edges if e["source"] in sub_ids and e["target"] in sub_ids]

        elif filter_mode == "amazon":
            target_parent = "parent_amazon"
            sub_ids = {target_parent}
            for e in self.edges:
                if e["target"] == target_parent or e["source"] == target_parent:
                    sub_ids.add(e["source"])
                    sub_ids.add(e["target"])
            for e in self.edges:
                if e["source"] in sub_ids or e["target"] in sub_ids:
                    sub_ids.add(e["source"])
                    sub_ids.add(e["target"])
            filtered_nodes = [n for n in self.nodes if n["id"] in sub_ids]
            filtered_edges = [e for e in self.edges if e["source"] in sub_ids and e["target"] in sub_ids]

        elif filter_mode == "streaming":
            streaming_mids = {"merch_youtube_premium", "merch_netflix_india", "merch_spotify_india", "merch_disney_hotstar", "merch_sony_liv", "merch_zee5", "merch_jiocinema_premium"}
            sub_ids = set(streaming_mids)
            for e in self.edges:
                if e["source"] in streaming_mids or e["target"] in streaming_mids:
                    sub_ids.add(e["source"])
                    sub_ids.add(e["target"])
            filtered_nodes = [n for n in self.nodes if n["id"] in sub_ids]
            filtered_edges = [e for e in self.edges if e["source"] in sub_ids and e["target"] in sub_ids]

        else: # "all"
            filtered_nodes = self.nodes
            filtered_edges = self.edges

        return {
            "filter_mode": filter_mode,
            "nodes": filtered_nodes,
            "edges": filtered_edges,
            "stats": {
                "total_nodes": len(filtered_nodes),
                "total_edges": len(filtered_edges),
                "parents": sum(1 for n in filtered_nodes if n["label"] == "Parent"),
                "merchants": sum(1 for n in filtered_nodes if n["label"] == "Merchant"),
                "mechanisms": sum(1 for n in filtered_nodes if n["label"] == "Mechanism"),
                "descriptors": sum(1 for n in filtered_nodes if n["label"] == "Descriptor"),
                "mandates": sum(1 for n in filtered_nodes if n["label"] == "Mandate")
            }
        }
