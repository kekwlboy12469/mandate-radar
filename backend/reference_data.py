"""
Mandate Radar Reference Knowledge Base:
Hand-assembled, strictly verified merchant catalog, parent corporate mapping,
descriptor regex resolution, billing mechanisms, and RBI/CCPA compliant cancellation & escalation trees.
"""

REFERENCE_MERCHANTS = [
    # Alphabet / Google footprint
    {
        "id": "youtube_premium",
        "name": "YouTube Premium",
        "category": "Entertainment & Streaming",
        "parent": "Alphabet Inc.",
        "parent_id": "alphabet",
        "official_website": "https://www.youtube.com/premium",
        "logo": "https://cdn.simpleicons.org/youtube/FF0000",
        "default_amount": 129.0,
        "supported_cadences": ["MONTHLY", "ANNUAL", "QUARTERLY"],
        "descriptors": [
            r"GOOGLE\*YOUTUBE\s+G\.CO/HELPPAY",
            r"GOOGLE\*YOUTUBE\s*PREMIUM",
            r"YOUTUBE\s*MEMBER",
            r"UPI/CR/\d+/GOOGLE/YOUTUBE",
            r"POS\s+DEBIT\s+GOOGLE\*YOUTUBE",
            r"GOOGLE\s*YOUTUBE\s*G\.CO/HELPPAY#",
            r"GOOGLE\s*SERVICES\s*YOUTUBE"
        ],
        "default_mechanism": "PLAY_STORE",
        "support_email": "support@google.com",
        "grievance_email": "grievance-officer-india@google.com",
        "cancellation_pitfall": "Cancelling or deleting the YouTube app on your phone does NOT stop the debit! Google processes this via Play Store Subscriptions or Google Payments."
    },
    {
        "id": "google_one",
        "name": "Google One (Cloud Storage)",
        "category": "Cloud & Productivity",
        "parent": "Alphabet Inc.",
        "parent_id": "alphabet",
        "official_website": "https://one.google.com",
        "logo": "https://cdn.simpleicons.org/google/4285F4",
        "default_amount": 130.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"GOOGLE\*GOOGLE\s+ONE\s+G\.CO/HELPPAY",
            r"GOOGLE\*STORAGE\s+G\.CO",
            r"GOOGLE\s+ONE\s+SUBSCRIPTION",
            r"UPI/CR/\d+/GOOGLE/ONE",
            r"GOOGLE\*DRIVE\s+G\.CO/HELPPAY"
        ],
        "default_mechanism": "PLAY_STORE",
        "support_email": "googleone-support@google.com",
        "grievance_email": "grievance-officer-india@google.com",
        "cancellation_pitfall": "Deleting files does not stop the monthly subscription. You must revoke via Google Play or one.google.com/settings."
    },
    {
        "id": "google_workspace",
        "name": "Google Workspace (GSuite)",
        "category": "Business & SaaS",
        "parent": "Alphabet Inc.",
        "parent_id": "alphabet",
        "official_website": "https://workspace.google.com",
        "logo": "https://cdn.simpleicons.org/googleworkspace/4285F4",
        "default_amount": 650.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"GOOGLE\*GSUITE_[A-Z0-9]+",
            r"GOOGLE\*WORKSPACE_[A-Z0-9]+",
            r"GOOGLE\s+CLOUD\s+WORKSPACE",
            r"POS\s+GOOGLE\*GSUITE"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "workspace-support@google.com",
        "grievance_email": "grievance-officer-india@google.com",
        "cancellation_pitfall": "Requires Admin Console credentials (admin.google.com) to cancel; bank-side block will suspend company domain emails."
    },
    {
        "id": "google_play_pass",
        "name": "Google Play Pass",
        "category": "Gaming & Apps",
        "parent": "Alphabet Inc.",
        "parent_id": "alphabet",
        "official_website": "https://play.google.com/about/play-pass",
        "logo": "https://cdn.simpleicons.org/googleplay/414141",
        "default_amount": 99.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"GOOGLE\*PLAY\s+PASS\s+G\.CO",
            r"GOOGLE\s*PLAYPASS\s+SUBS",
            r"UPI/CR/\d+/GOOGLE/PLAY"
        ],
        "default_mechanism": "PLAY_STORE",
        "support_email": "play-support@google.com",
        "grievance_email": "grievance-officer-india@google.com",
        "cancellation_pitfall": "Manage directly in Play Store under Payments & Subscriptions."
    },

    # Amazon.com footprint
    {
        "id": "amazon_prime",
        "name": "Amazon Prime India",
        "category": "E-Commerce & Entertainment",
        "parent": "Amazon.com Inc.",
        "parent_id": "amazon",
        "official_website": "https://www.amazon.in/prime",
        "logo": "https://cdn.simpleicons.org/amazon/FF9900",
        "default_amount": 299.0,
        "supported_cadences": ["MONTHLY", "QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"AMZN\s+PRIME\s+IN\*\d+",
            r"AMAZON\s+PRIME\s+MEMBER",
            r"AMZN\*PRIME\s+RECURRING",
            r"AMAZON\s+SELLER\s+SERVICES\s+PRIME",
            r"UPI/CR/\d+/AMAZON/PRIME",
            r"ACH\s+D\s+AMAZON\s+PAY\s+INDIA"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "cis@amazon.com",
        "grievance_email": "grievance-officer@amazon.in",
        "cancellation_pitfall": "Amazon Prime hides the cancellation button behind 3 confirmation screens ('Keep My Benefits'). Complete all 3 screens until confirmation number is displayed."
    },
    {
        "id": "audible_india",
        "name": "Audible India",
        "category": "Audiobooks & Media",
        "parent": "Amazon.com Inc.",
        "parent_id": "amazon",
        "official_website": "https://www.audible.in",
        "logo": "https://cdn.simpleicons.org/audible/F8991C",
        "default_amount": 199.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"AUDIBLE\*IN\*\d+",
            r"AUDIBLE\s+MEDIA\s+IN",
            r"AMZN\*AUDIBLE\s+SUBS",
            r"UPI/CR/\d+/AUDIBLE"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "customersupport@audible.in",
        "grievance_email": "grievance-officer@amazon.in",
        "cancellation_pitfall": "Unused credits expire when you cancel Audible membership! Spend your accumulated credits before clicking cancel."
    },
    {
        "id": "aws_cloud",
        "name": "Amazon Web Services (AWS)",
        "category": "Cloud & Infrastructure",
        "parent": "Amazon.com Inc.",
        "parent_id": "amazon",
        "official_website": "https://aws.amazon.com",
        "logo": "https://cdn.simpleicons.org/amazonwebservices/232F3E",
        "default_amount": 1200.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"AWS\*EMEA\s+ONLINE",
            r"AMAZON\s+WEB\s+SERVICES\s+AWS",
            r"AMZN\s+AWS\s+SERVICES",
            r"POS\s+DEBIT\s+AMAZON\s+WEB\s+SERVICES"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "aws-verification@amazon.com",
        "grievance_email": "grievance-officer@amazon.in",
        "cancellation_pitfall": "Stopping credit card standing instructions without terminating EC2/RDS instances will incur ongoing debt collections and account suspension."
    },
    {
        "id": "kindle_unlimited",
        "name": "Kindle Unlimited",
        "category": "Books & Reading",
        "parent": "Amazon.com Inc.",
        "parent_id": "amazon",
        "official_website": "https://www.amazon.in/kindle-dbs/hz/signup",
        "logo": "https://cdn.simpleicons.org/amazon/FF9900",
        "default_amount": 169.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"KINDLE\*UNLIMITED\s+IN",
            r"AMZN\*KINDLE\s+UNLIMITED",
            r"AMAZON\s+KINDLE\s+SUB"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "kindle-cs-support@amazon.in",
        "grievance_email": "grievance-officer@amazon.in",
        "cancellation_pitfall": "Borrowing list locks instantly; downloaded books disappear from Kindle device upon cancellation billing cycle end."
    },

    # Netflix Inc
    {
        "id": "netflix_india",
        "name": "Netflix India",
        "category": "Entertainment & Streaming",
        "parent": "Netflix Inc.",
        "parent_id": "netflix",
        "official_website": "https://www.netflix.com",
        "logo": "https://cdn.simpleicons.org/netflix/E50914",
        "default_amount": 499.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"NETFLIX\.COM\s+NETFLIX\s+ENTERTAINMENT",
            r"NETFLIX\s+ENTERTAINMENT\s+SVCS",
            r"UPI/CR/\d+/NETFLIX/AUTOPAY",
            r"NETFLIX\s+INDIA\s+MUMBAI",
            r"POS\s+DEBIT\s+NETFLIX\.COM",
            r"NETFLIX\s+SUBSCRIPTION\s+MUM"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "info@netflix.com",
        "grievance_email": "grievance-india@netflix.com",
        "cancellation_pitfall": "Cancelling pauses debits at current period end. If you reactivate on any device by accident, the mandate is silently re-engaged."
    },

    # Spotify AB
    {
        "id": "spotify_india",
        "name": "Spotify Premium India",
        "category": "Music & Podcasts",
        "parent": "Spotify Technology S.A.",
        "parent_id": "spotify",
        "official_website": "https://www.spotify.com",
        "logo": "https://cdn.simpleicons.org/spotify/1ED760",
        "default_amount": 119.0,
        "supported_cadences": ["MONTHLY", "ANNUAL", "QUARTERLY"],
        "descriptors": [
            r"SPOTIFY\s+INDIA\s+MUMBAI",
            r"SPOTIFY\*PREMIUM\s+IN",
            r"UPI/CR/\d+/SPOTIFY/PREMIUM",
            r"PAYTM\*SPOTIFY\s+MANDATE",
            r"SPOTIFY\s+AB\s+STOCKHOLM",
            r"POS\s+SPOTIFY\s+INDIA"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@spotify.com",
        "grievance_email": "grievance-india@spotify.com",
        "cancellation_pitfall": "If subscribed through Apple App Store or Google Play, you cannot cancel from Spotify website. You must revoke via Apple/Google subscriptions."
    },

    # The Walt Disney Company / Star India
    {
        "id": "disney_hotstar",
        "name": "Disney+ Hotstar (Star India)",
        "category": "Entertainment & Streaming",
        "parent": "The Walt Disney Company",
        "parent_id": "disney",
        "official_website": "https://www.hotstar.com",
        "logo": "https://cdn.simpleicons.org/disneyplus/000000",
        "default_amount": 299.0,
        "supported_cadences": ["MONTHLY", "QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"NOVI\s+DIGITAL\s+HOTSTAR",
            r"STAR\s+INDIA\s+HOTSTAR\s+SUB",
            r"UPI/CR/\d+/HOTSTAR/AUTOPAY",
            r"HOTSTAR\*PREMIUM\s+IN",
            r"DISNEY\s+HOTSTAR\s+MUMBAI"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "subscription@hotstar.com",
        "grievance_email": "grievanceofficer@hotstar.com",
        "cancellation_pitfall": "Often bundled with telecom recharges (Jio/Airtel). If billed through telecom provider, cancel in the Telco app, not Hotstar."
    },

    # Apple Inc footprint
    {
        "id": "apple_services",
        "name": "Apple Services (iCloud / Apple One / Music)",
        "category": "Cloud & Ecosystem",
        "parent": "Apple Inc.",
        "parent_id": "apple",
        "official_website": "https://reportaproblem.apple.com",
        "logo": "https://cdn.simpleicons.org/apple/000000",
        "default_amount": 75.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"APPLE\.COM/BILL\s+ITUNES\.COM",
            r"APPLE\s+SERVICES\s+RECURRING",
            r"APPLE\.COM/BILL\s+IRELAND",
            r"POS\s+APPLE\.COM/BILL",
            r"UPI/CR/\d+/APPLE/ITUNES"
        ],
        "default_mechanism": "APP_STORE",
        "support_email": "appleid_iien@email.apple.com",
        "grievance_email": "grievance-officer-india@apple.com",
        "cancellation_pitfall": "Apple does not show individual app names on card statements—it simply lumps them as 'APPLE.COM/BILL'. Check reportaproblem.apple.com to see which specific app triggered it."
    },

    # Microsoft Corporation footprint
    {
        "id": "microsoft_365",
        "name": "Microsoft 365 (Office / OneDrive)",
        "category": "Cloud & Productivity",
        "parent": "Microsoft Corporation",
        "parent_id": "microsoft",
        "official_website": "https://account.microsoft.com/services",
        "logo": "https://cdn.simpleicons.org/microsoft/00A4EF",
        "default_amount": 489.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"MSFT\s+\*E0[0-9A-Z]+\s+MSBILL\.INFO",
            r"MICROSOFT\*OFFICE\s+365",
            r"MSFT\s+\*OFFICE\s+SUBSCRIPTION",
            r"MSBILL\.INFO\s+BILLING",
            r"MICROSOFT\s+REGIONAL\s+SALES"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "msbill@microsoft.com",
        "grievance_email": "grievance-officer@microsoft.com",
        "cancellation_pitfall": "Requires turning off 'Recurring Billing' in account.microsoft.com/services at least 48 hours prior to renewal date."
    },
    {
        "id": "xbox_game_pass",
        "name": "Xbox Game Pass",
        "category": "Gaming",
        "parent": "Microsoft Corporation",
        "parent_id": "microsoft",
        "official_website": "https://www.xbox.com/gamepass",
        "logo": "https://cdn.simpleicons.org/xbox/107C10",
        "default_amount": 549.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"MSFT\s+\*XBOX\s+GAME\s+PASS",
            r"MICROSOFT\*XBOX\s+LIVE",
            r"MSBILL\.INFO\*XBOX"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@xbox.com",
        "grievance_email": "grievance-officer@microsoft.com",
        "cancellation_pitfall": "Cancelling on console often errors if 2FA prompt fails. Better to cancel via web browser on account.microsoft.com."
    },
    {
        "id": "github_copilot",
        "name": "GitHub Copilot / Pro",
        "category": "Developer Tools",
        "parent": "Microsoft Corporation",
        "parent_id": "microsoft",
        "official_website": "https://github.com/settings/billing",
        "logo": "https://cdn.simpleicons.org/github/181717",
        "default_amount": 830.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"GITHUB\s+INC\s+SAN\s+FRANCISCO",
            r"GITHUB\*COPILOT\s+SUBS",
            r"POS\s+DEBIT\s+GITHUB\s+INC"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@github.com",
        "grievance_email": "grievance-officer@microsoft.com",
        "cancellation_pitfall": "Seat licenses remain billed unless seat assignment is explicitly revoked under billing settings."
    },
    {
        "id": "linkedin_premium",
        "name": "LinkedIn Premium",
        "category": "Professional & Career",
        "parent": "Microsoft Corporation",
        "parent_id": "microsoft",
        "official_website": "https://www.linkedin.com/premium",
        "logo": "https://cdn.simpleicons.org/linkedin/0A66C2",
        "default_amount": 1499.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"LINKEDIN\s+IRELAND\s+SUBSCRIPTION",
            r"LINKEDIN\*PREMIUM\s+IN",
            r"LINKEDIN\s+CORP\s+CALIFORNIA",
            r"POS\s+DEBIT\s+LINKEDIN\s+IRELAND"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "linkedin_support@linkedin.com",
        "grievance_email": "grievance-officer@linkedin.com",
        "cancellation_pitfall": "Free trials automatically renew at ₹1,499+/month. Cancellation must be performed via Account Settings > Subscriptions."
    },

    # Bundl Technologies (Swiggy)
    {
        "id": "swiggy_one",
        "name": "Swiggy One Membership",
        "category": "Food & Quick Commerce",
        "parent": "Bundl Technologies Pvt Ltd",
        "parent_id": "swiggy_corp",
        "official_website": "https://www.swiggy.com",
        "logo": "https://cdn.simpleicons.org/swiggy/FC8019",
        "default_amount": 299.0,
        "supported_cadences": ["QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"BUNDL\s+TECHNOLOGIES\s+SWIGGY\s+ONE",
            r"SWIGGY\s+ONE\s+MEMBERSHIP",
            r"UPI/CR/\d+/SWIGGY/ONEAUTOPAY",
            r"BUNDL\s+TECH\*SWIGGY\s+RECURRING"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@swiggy.in",
        "grievance_email": "grievance-officer@swiggy.in",
        "cancellation_pitfall": "Swiggy One AutoPay does not offer in-app refund for mid-term cancellation. Revoke the mandate in UPI app (GPay/PhonePe) immediately to prevent renewal."
    },

    # Zomato Limited / Blinkit
    {
        "id": "zomato_gold",
        "name": "Zomato Gold VIP",
        "category": "Dining & Delivery",
        "parent": "Eternal Limited (Zomato Ltd)",
        "parent_id": "zomato_corp",
        "official_website": "https://www.zomato.com/gold",
        "logo": "https://cdn.simpleicons.org/zomato/CB202D",
        "default_amount": 199.0,
        "supported_cadences": ["QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"ZOMATO\s+LIMITED\s+GOLD\s+MANDATE",
            r"ZOMATO\s+MEDIA\s+PVT\s+LTD\s+GOLD",
            r"UPI/CR/\d+/ZOMATO/GOLD_AUTOPAY",
            r"ZOMATO\*GOLD\s+MEMBERSHIP"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "order@zomato.com",
        "grievance_email": "grievanceofficer@zomato.com",
        "cancellation_pitfall": "Auto-renewal triggers 24 hours prior to expiration date. Revoke mandate inside your payment app."
    },

    # OpenAI LLC
    {
        "id": "chatgpt_plus",
        "name": "ChatGPT Plus (OpenAI)",
        "category": "AI & Technology",
        "parent": "OpenAI LLC",
        "parent_id": "openai",
        "official_website": "https://chatgpt.com",
        "logo": "https://cdn.simpleicons.org/openai/000000",
        "default_amount": 1999.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"OPENAI\s+\*CHATGPT\s+SUBSCRIPTION",
            r"OPENAI\s+LLC\s+SAN\s+FRANCISCO",
            r"POS\s+DEBIT\s+OPENAI\s+\*CHATGPT",
            r"STRIPE\*OPENAI\s+CHATGPT"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@openai.com",
        "grievance_email": "privacy@openai.com",
        "cancellation_pitfall": "Billed in USD ($20/mo + GST = ~₹1,999 to ₹2,050). Currency fluctuations make amounts drift slightly; cancel via chatgpt.com > My Plan."
    },

    # Times Internet
    {
        "id": "times_prime",
        "name": "Times Prime",
        "category": "Lifestyle & Bundles",
        "parent": "Times Internet (Bennett, Coleman & Co.)",
        "parent_id": "times_group",
        "official_website": "https://www.timesprime.com",
        "logo": "https://cdn.simpleicons.org/times/D2232A",
        "default_amount": 1199.0,
        "supported_cadences": ["ANNUAL"],
        "descriptors": [
            r"TIMES\s+INTERNET\s+LTD\s+TIMESPRIME",
            r"TIMES\s+PRIME\s+ANNUAL\s+SUB",
            r"UPI/CR/\d+/TIMESINTERNET/MANDATE",
            r"ACH\s+D\s+TIMES\s+INTERNET\s+LTD"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@timesprime.com",
        "grievance_email": "grievance@timesinternet.in",
        "cancellation_pitfall": "Annual AutoPay triggers without visible notification on some apps. Check UPI AutoPay registered mandates."
    },

    # Cult.fit / Curefoods
    {
        "id": "cult_fit",
        "name": "Cult.fit (Cultpass)",
        "category": "Fitness & Health",
        "parent": "Curefit Healthcare Pvt Ltd",
        "parent_id": "curefit",
        "official_website": "https://www.cult.fit",
        "logo": "https://cdn.simpleicons.org/fitbit/00B0B9",
        "default_amount": 1450.0,
        "supported_cadences": ["MONTHLY", "QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"CUREFIT\s+HEALTHCARE\s+PVT\s+LTD",
            r"CULT\.FIT\s+MEMBERSHIP\s+AUTOPAY",
            r"UPI/CR/\d+/CUREFIT/AUTOPAY",
            r"ACH\s+D\s+CUREFIT\s+HEALTHCARE"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "hello@cult.fit",
        "grievance_email": "grievance@cult.fit",
        "cancellation_pitfall": "Cult monthly pass often uses NACH mandate. Cancelling NACH requires submitting mandate cancellation to your bank if app fails."
    },

    # Sony Group Corp
    {
        "id": "sony_liv",
        "name": "Sony LIV Premium",
        "category": "Entertainment & Streaming",
        "parent": "Sony Group Corporation",
        "parent_id": "sony",
        "official_website": "https://www.sonyliv.com",
        "logo": "https://cdn.simpleicons.org/sony/000000",
        "default_amount": 299.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"CULVER\s+MAX\s+ENTERTAINMENT\s+SONYLIV",
            r"SONY\s+LIV\s+DIGITAL\s+MUMBAI",
            r"UPI/CR/\d+/SONYLIV/AUTOPAY",
            r"SONY\s+PICTURES\s+NETWORKS\s+IN"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@sonyliv.com",
        "grievance_email": "grievanceofficer@setindia.com",
        "cancellation_pitfall": "Culver Max Entertainment is the legal billing entity descriptor."
    },

    # Zee Entertainment
    {
        "id": "zee5",
        "name": "ZEE5 Premium",
        "category": "Entertainment & Streaming",
        "parent": "Zee Entertainment Enterprises Ltd",
        "parent_id": "zee",
        "official_website": "https://www.zee5.com",
        "logo": "https://cdn.simpleicons.org/zee5/252525",
        "default_amount": 149.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"ZEE\s+ENTERTAINMENT\s+ENT\s+LTD",
            r"ZEE5\s+PREMIUM\s+SUBSCRIPTION",
            r"UPI/CR/\d+/ZEE5/AUTOPAY"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support.in@zee5.com",
        "grievance_email": "grievanceofficer@zee.com",
        "cancellation_pitfall": "Must turn off auto-renewal in My Subscriptions before the last 48 hours of subscription."
    },

    # Reliance Jio
    {
        "id": "jiocinema_premium",
        "name": "JioCinema Premium",
        "category": "Entertainment & Streaming",
        "parent": "Reliance Industries / Jio Platforms",
        "parent_id": "reliance_jio",
        "official_website": "https://www.jiocinema.com",
        "logo": "https://cdn.simpleicons.org/jio/00388A",
        "default_amount": 29.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"VIACOM18\s+MEDIA\s+PVT\s+LTD\s+JIOCINEMA",
            r"JIOCINEMA\s+PREMIUM\s+AUTO",
            r"UPI/CR/\d+/JIOCINEMA/RECURRING",
            r"JIO\s+PLATFORMS\s+LTD\s+MUMBAI"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@jiocinema.com",
        "grievance_email": "grievanceofficer@jiocinema.com",
        "cancellation_pitfall": "Viacom18 Media descriptor is often used on statement."
    },

    # Bharti Airtel
    {
        "id": "airtel_xstream",
        "name": "Airtel Xstream Play",
        "category": "Telecom & OTT",
        "parent": "Bharti Airtel Limited",
        "parent_id": "airtel",
        "official_website": "https://www.airtelxstream.in",
        "logo": "https://cdn.simpleicons.org/airtel/FF0000",
        "default_amount": 149.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"BHARTI\s+AIRTEL\s+LTD\s+XSTREAM",
            r"AIRTEL\s+XSTREAM\s+PACK",
            r"ACH\s+D\s+BHARTI\s+AIRTEL\s+LTD"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "digitalcare@airtel.com",
        "grievance_email": "nodalofficer@airtel.com",
        "cancellation_pitfall": "Linked to broadband/SIM post-paid bill; must be removed in Airtel Thanks app > Add-ons."
    },

    # Tata Sons
    {
        "id": "tata_play_binge",
        "name": "Tata Play Binge",
        "category": "DTH & OTT",
        "parent": "Tata Sons (Tata Play Ltd)",
        "parent_id": "tata_group",
        "official_website": "https://www.tataplay.com",
        "logo": "https://cdn.simpleicons.org/tata/005A9C",
        "default_amount": 299.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"TATA\s+PLAY\s+LIMITED\s+BINGE",
            r"TATA\s+SKY\s+LTD\s+MUMBAI",
            r"UPI/CR/\d+/TATAPLAY/MANDATE",
            r"ACH\s+D\s+TATA\s+PLAY\s+LTD"
        ],
        "default_mechanism": "BANK_NACH",
        "support_email": "help@tataplay.com",
        "grievance_email": "nodal@tataplay.com",
        "cancellation_pitfall": "Binge subscriptions billed via NACH require bank mandate revocation if app support fails."
    },

    # Adobe Inc
    {
        "id": "adobe_creative_cloud",
        "name": "Adobe Creative Cloud",
        "category": "Design & Software",
        "parent": "Adobe Inc.",
        "parent_id": "adobe",
        "official_website": "https://account.adobe.com/plans",
        "logo": "https://cdn.simpleicons.org/adobe/FF0000",
        "default_amount": 4230.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"ADOBE\s+\*CREATIVE\s+CLOUD",
            r"ADOBE\s+SYSTEMS\s+IRELAND\s+LTD",
            r"POS\s+DEBIT\s+ADOBE\s+SYSTEMS",
            r"ADOBE\s+\*[0-9A-Z]+\s+IRELAND"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@adobe.com",
        "grievance_email": "compliance@adobe.com",
        "cancellation_pitfall": "Adobe has notorious early cancellation termination fees (up to 50% of remaining annual commitment). Switching plans first or contacting agent waives this fee."
    },

    # Canva Pty Ltd
    {
        "id": "canva_pro",
        "name": "Canva Pro",
        "category": "Design & Productivity",
        "parent": "Canva Pty Ltd",
        "parent_id": "canva",
        "official_website": "https://www.canva.com/settings/billing",
        "logo": "https://cdn.simpleicons.org/canva/00C4CC",
        "default_amount": 499.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"CANVA\s+PTY\s+LTD\s+SYDNEY",
            r"CANVA\*PRO\s+SUBSCRIPTION",
            r"POS\s+CANVA\s+PTY\s+LTD"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@canva.com",
        "grievance_email": "support@canva.com",
        "cancellation_pitfall": "Team features remain active until period end; cancel via Account Settings > Billing."
    },

    # Notion Labs Inc
    {
        "id": "notion_plus",
        "name": "Notion Plus",
        "category": "Productivity & Docs",
        "parent": "Notion Labs Inc.",
        "parent_id": "notion",
        "official_website": "https://www.notion.so/settings",
        "logo": "https://cdn.simpleicons.org/notion/000000",
        "default_amount": 830.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"NOTION\s+LABS\s+INC\s+SAN\s+FRANCISCO",
            r"NOTION\*PLUS\s+SUBSCRIPTION",
            r"POS\s+DEBIT\s+NOTION\s+LABS"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "team@makenotion.com",
        "grievance_email": "privacy@makenotion.com",
        "cancellation_pitfall": "Workspace downgrade requires removing members if exceeding free tier workspace limits."
    },

    # Duolingo Inc
    {
        "id": "duolingo_super",
        "name": "Duolingo Super",
        "category": "Education & Learning",
        "parent": "Duolingo Inc.",
        "parent_id": "duolingo",
        "official_website": "https://www.duolingo.com/settings/super",
        "logo": "https://cdn.simpleicons.org/duolingo/58CC02",
        "default_amount": 169.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"DUOLINGO\s+INC\s+PITTSBURGH",
            r"DUOLINGO\*SUPER\s+SUBS",
            r"GOOGLE\*DUOLINGO\s+G\.CO",
            r"APPLE\.COM/BILL\s+DUOLINGO"
        ],
        "default_mechanism": "PLAY_STORE",
        "support_email": "super-support@duolingo.com",
        "grievance_email": "support@duolingo.com",
        "cancellation_pitfall": "90% of Duolingo subscriptions in India are created inside Android/iOS, so cancelling inside app settings will just redirect you to Play/App store."
    },

    # Truecaller AB
    {
        "id": "truecaller_premium",
        "name": "Truecaller Premium",
        "category": "Utilities & Security",
        "parent": "Truecaller AB",
        "parent_id": "truecaller",
        "official_website": "https://www.truecaller.com",
        "logo": "https://cdn.simpleicons.org/truecaller/0087FF",
        "default_amount": 79.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"TRUE\s+SOFTWARE\s+SCANDINAVIA\s+AB",
            r"TRUECALLER\s+PREMIUM\s+IN",
            r"UPI/CR/\d+/TRUECALLER/PREMIUM",
            r"GOOGLE\*TRUECALLER\s+G\.CO"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@truecaller.com",
        "grievance_email": "grievance.officer@truecaller.com",
        "cancellation_pitfall": "Uninstalling Truecaller or turning off caller ID does NOT terminate subscription."
    },

    # Urban Company
    {
        "id": "urban_company_plus",
        "name": "Urban Company Plus",
        "category": "Home & Services",
        "parent": "Urban Company (UrbanClap Technologies)",
        "parent_id": "urban_company",
        "official_website": "https://www.urbancompany.com",
        "logo": "https://cdn.simpleicons.org/urbancompany/000000",
        "default_amount": 299.0,
        "supported_cadences": ["QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"URBANCLAP\s+TECHNOLOGIES\s+INDIA",
            r"URBAN\s+COMPANY\s+PLUS\s+MEMBER",
            r"UPI/CR/\d+/URBANCOMPANY/PLUS"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@urbancompany.com",
        "grievance_email": "grievanceofficer@urbancompany.com",
        "cancellation_pitfall": "Revoke mandate inside UPI app to stop quarterly rollover."
    },

    # ICICI Lombard / Insurance Mandates
    {
        "id": "icici_lombard",
        "name": "ICICI Lombard Health / Auto Shield",
        "category": "Insurance & Protection",
        "parent": "ICICI Bank Ltd",
        "parent_id": "icici_group",
        "official_website": "https://www.icicilombard.com",
        "logo": "https://cdn.simpleicons.org/icicibank/F37021",
        "default_amount": 950.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"ACH\s+D\s+ICICI\s+LOMBARD\s+GIC",
            r"ICICI\s+LOMBARD\s+PREMIUM\s+NACH",
            r"NACH/ICICILOM/\d+/MANDATE"
        ],
        "default_mechanism": "BANK_NACH",
        "support_email": "customersupport@icicilombard.com",
        "grievance_email": "gro@icicilombard.com",
        "cancellation_pitfall": "Cancelling policy debit mandate without notifying insurer will cause policy lapse and forfeiture of accumulated no-claim bonuses."
    },

    # HDFC Ergo / Life
    {
        "id": "hdfc_ergo",
        "name": "HDFC ERGO General Insurance",
        "category": "Insurance & Protection",
        "parent": "HDFC Bank Ltd",
        "parent_id": "hdfc_group",
        "official_website": "https://www.hdfcergo.com",
        "logo": "https://cdn.simpleicons.org/hdfcbank/004C8F",
        "default_amount": 1200.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"ACH\s+D\s+HDFC\s+ERGO\s+GEN\s+INS",
            r"NACH/HDFCERGO/\d+",
            r"HDFC\s+LIFE\s+INSURANCE\s+NACH"
        ],
        "default_mechanism": "BANK_NACH",
        "support_email": "care@hdfcergo.com",
        "grievance_email": "grievance@hdfcergo.com",
        "cancellation_pitfall": "Requires official policy surrender or mandate cancellation form to avoid insurer negative credit reporting."
    },

    # Bajaj Finserv EMI / Mandate
    {
        "id": "bajaj_finserv",
        "name": "Bajaj Finserv Consumer EMI",
        "category": "Lending & Loans",
        "parent": "Bajaj Finserv Ltd",
        "parent_id": "bajaj_group",
        "official_website": "https://www.bajajfinserv.in",
        "logo": "https://cdn.simpleicons.org/bajaj/005696",
        "default_amount": 2499.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"ACH\s+D\s+BAJAJ\s+FINANCE\s+LTD",
            r"BAJAJ\s+FINSERV\s+EMI\s+MANDATE",
            r"NACH/BAJAJFIN/\d+"
        ],
        "default_mechanism": "BANK_NACH",
        "support_email": "wecare@bajajfinserv.in",
        "grievance_email": "grievanceredressal@bajajfinserv.in",
        "cancellation_pitfall": "Cancelling a loan EMI NACH mandate before full repayment will attract ₹450-₹750 bounce charges and hurt CIBIL score!"
    },

    # Grammarly Inc
    {
        "id": "grammarly_premium",
        "name": "Grammarly Premium",
        "category": "Productivity & Writing",
        "parent": "Grammarly Inc.",
        "parent_id": "grammarly",
        "official_website": "https://account.grammarly.com/subscription",
        "logo": "https://cdn.simpleicons.org/grammarly/15C39A",
        "default_amount": 999.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"GRAMMARLY\s+\*PREMIUM\s+SAN\s+FRANCISCO",
            r"GRAMMARLY\s+INC\s+SUBSCRIPTION",
            r"POS\s+DEBIT\s+GRAMMARLY"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@grammarly.com",
        "grievance_email": "support@grammarly.com",
        "cancellation_pitfall": "Cancel at least 24 hours before next billing date to avoid annual renewal charge."
    },

    # 1Password (AgileBits)
    {
        "id": "onepassword",
        "name": "1Password Families / Individual",
        "category": "Utilities & Security",
        "parent": "AgileBits Inc.",
        "parent_id": "agilebits",
        "official_website": "https://my.1password.com/billing",
        "logo": "https://cdn.simpleicons.org/1password/0A85EA",
        "default_amount": 350.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"AGILEBITS\s+INC\s+1PASSWORD",
            r"1PASSWORD\*SUBSCRIPTION",
            r"POS\s+AGILEBITS\s+TORONTO"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@1password.com",
        "grievance_email": "privacy@1password.com",
        "cancellation_pitfall": "Export your vault and emergency kit BEFORE terminating your subscription account."
    },

    # Nord Security (NordVPN)
    {
        "id": "nordvpn",
        "name": "NordVPN / NordPass",
        "category": "Privacy & VPN",
        "parent": "Nord Security",
        "parent_id": "nord_security",
        "official_website": "https://my.nordaccount.com",
        "logo": "https://cdn.simpleicons.org/nordvpn/4687FF",
        "default_amount": 420.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"NORDVPN\s+SA\s+PANAMA",
            r"NORD\s+SECURITY\s+SUBSCRIPTION",
            r"POS\s+DEBIT\s+NORDVPN"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@nordvpn.com",
        "grievance_email": "support@nordvpn.com",
        "cancellation_pitfall": "Auto-renewal is enabled by default with a higher price after the first year promotional rate."
    },

    # Chess.com
    {
        "id": "chess_com",
        "name": "Chess.com Diamond / Platinum",
        "category": "Gaming & Strategy",
        "parent": "Chess.com LLC",
        "parent_id": "chess_com",
        "official_website": "https://www.chess.com/membership",
        "logo": "https://cdn.simpleicons.org/chessdotcom/7FA650",
        "default_amount": 399.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"CHESS\.COM\s+MEMBERSHIP",
            r"CHESS\.COM\s+PALO\s+ALTO",
            r"GOOGLE\*CHESS\.COM\s+G\.CO",
            r"APPLE\.COM/BILL\s+CHESS\.COM"
        ],
        "default_mechanism": "PLAY_STORE",
        "support_email": "support@chess.com",
        "grievance_email": "support@chess.com",
        "cancellation_pitfall": "Check whether purchase was made on web or inside Android/iOS app."
    },

    # Strava Inc
    {
        "id": "strava",
        "name": "Strava Premium Summit",
        "category": "Fitness & Cycling",
        "parent": "Strava Inc.",
        "parent_id": "strava",
        "official_website": "https://www.strava.com/settings/billing",
        "logo": "https://cdn.simpleicons.org/strava/FC4C02",
        "default_amount": 299.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"STRAVA\s+INC\s+SAN\s+FRANCISCO",
            r"STRAVA\*SUBSCRIPTION",
            r"GOOGLE\*STRAVA\s+G\.CO"
        ],
        "default_mechanism": "PLAY_STORE",
        "support_email": "support@strava.com",
        "grievance_email": "support@strava.com",
        "cancellation_pitfall": "Cancelling preserves your past athletic activity data; premium analytics features revert to free tier."
    },

    # Headspace Inc
    {
        "id": "headspace",
        "name": "Headspace Mindfulness",
        "category": "Mental Wellness & Health",
        "parent": "Headspace Inc.",
        "parent_id": "headspace",
        "official_website": "https://www.headspace.com/settings/subscription",
        "logo": "https://cdn.simpleicons.org/headspace/FF6138",
        "default_amount": 149.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"HEADSPACE\s+INC\s+SANTA\s+MONICA",
            r"HEADSPACE\*SUBSCRIPTION",
            r"GOOGLE\*HEADSPACE\s+G\.CO",
            r"APPLE\.COM/BILL\s+HEADSPACE"
        ],
        "default_mechanism": "PLAY_STORE",
        "support_email": "help@headspace.com",
        "grievance_email": "help@headspace.com",
        "cancellation_pitfall": "Free trial converts to full annual charge automatically if not stopped 24 hours prior."
    },

    # Calm.com
    {
        "id": "calm",
        "name": "Calm Sleep & Meditation",
        "category": "Mental Wellness & Health",
        "parent": "Calm.com Inc.",
        "parent_id": "calm_com",
        "official_website": "https://www.calm.com/settings/manage-subscription",
        "logo": "https://cdn.simpleicons.org/calm/4A90E2",
        "default_amount": 349.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"CALM\.COM\s+INC\s+SAN\s+FRANCISCO",
            r"CALM\*SUBSCRIPTION",
            r"GOOGLE\*CALM\s+G\.CO"
        ],
        "default_mechanism": "PLAY_STORE",
        "support_email": "support@calm.com",
        "grievance_email": "support@calm.com",
        "cancellation_pitfall": "Often converted from Instagram ad trial to ₹3,500 annual charge."
    },

    # Blinkist
    {
        "id": "blinkist",
        "name": "Blinkist Book Summaries",
        "category": "Books & Learning",
        "parent": "Blinkist (Go1 Pty Ltd)",
        "parent_id": "blinkist_corp",
        "official_website": "https://www.blinkist.com/en/settings",
        "logo": "https://cdn.simpleicons.org/blinkist/2CE080",
        "default_amount": 299.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"BLINKS\s+LABS\s+GMBH\s+BERLIN",
            r"BLINKIST\*SUBSCRIPTION",
            r"GOOGLE\*BLINKIST\s+G\.CO"
        ],
        "default_mechanism": "PLAY_STORE",
        "support_email": "support@blinkist.com",
        "grievance_email": "support@blinkist.com",
        "cancellation_pitfall": "Blinks Labs GmbH is the legal German entity name shown on bank slips."
    },

    # Zoom Video Communications
    {
        "id": "zoom_video",
        "name": "Zoom Workplace Pro",
        "category": "Video Conferencing & SaaS",
        "parent": "Zoom Video Communications Inc.",
        "parent_id": "zoom_corp",
        "official_website": "https://zoom.us/billing",
        "logo": "https://cdn.simpleicons.org/zoom/2D8CFF",
        "default_amount": 1300.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"ZOOM\.US\s+\*[0-9A-Z]+\s+SAN\s+JOSE",
            r"ZOOM\s+VIDEO\s+COMMUNICATIONS",
            r"POS\s+DEBIT\s+ZOOM\.US"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "billing@zoom.us",
        "grievance_email": "privacy@zoom.us",
        "cancellation_pitfall": "Must click through 'Cancel Subscription' in web billing; meetings revert to 40-minute limit."
    },

    # Additional Indian & Global Merchants to complete 75+ Reference Knowledge Graph
    {
        "id": "jiosaavn_pro",
        "name": "JioSaavn Pro",
        "category": "Music & Podcasts",
        "parent": "Reliance Industries / Jio Platforms",
        "parent_id": "reliance_jio",
        "official_website": "https://www.jiosaavn.com/pro",
        "logo": "https://cdn.simpleicons.org/jio/00388A",
        "default_amount": 99.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"JIOSAAVN\s+PRO\s+MUMBAI",
            r"SAAVN\s+MEDIA\s+PVT\s+LTD",
            r"UPI/CR/\d+/SAAVN/PRO",
            r"RELIANCE\s+JIOSAAVN"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "feedback@jiosaavn.com",
        "grievance_email": "grievanceofficer@jiosaavn.com",
        "cancellation_pitfall": "Saavn Media Pvt Ltd is the billing entity descriptor."
    },
    {
        "id": "wynk_music",
        "name": "Wynk Music Premium",
        "category": "Music & Podcasts",
        "parent": "Bharti Airtel Limited",
        "parent_id": "airtel",
        "official_website": "https://wynk.in/music",
        "logo": "https://cdn.simpleicons.org/airtel/FF0000",
        "default_amount": 49.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"WYNK\s+LIMITED\s+AIRTEL",
            r"WYNK\s+MUSIC\s+SUBSCRIPTION",
            r"UPI/CR/\d+/WYNKMUSIC/MANDATE"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "contact@wynk.in",
        "grievance_email": "nodalofficer@airtel.com",
        "cancellation_pitfall": "Billed through Airtel broadband or mobile bill; cancel in Wynk app > My Account."
    },
    {
        "id": "gaana_plus",
        "name": "Gaana Plus",
        "category": "Music & Audio",
        "parent": "Times Internet (Bennett, Coleman & Co.)",
        "parent_id": "times_group",
        "official_website": "https://gaana.com",
        "logo": "https://cdn.simpleicons.org/times/D2232A",
        "default_amount": 99.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"GAMMA\s+GAANA\s+LTD\s+NEW\s+DELHI",
            r"GAANA\s+PLUS\s+SUBSCRIPTION",
            r"UPI/CR/\d+/GAANA/PLUS"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "feedback@gaana.com",
        "grievance_email": "grievance@timesinternet.in",
        "cancellation_pitfall": "Gamma Gaana Ltd is the billing descriptor."
    },
    {
        "id": "et_prime",
        "name": "Economic Times Prime (ET Prime)",
        "category": "Business & News",
        "parent": "Times Internet (Bennett, Coleman & Co.)",
        "parent_id": "times_group",
        "official_website": "https://economictimes.indiatimes.com/prime",
        "logo": "https://cdn.simpleicons.org/times/D2232A",
        "default_amount": 399.0,
        "supported_cadences": ["QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"TIMES\s+INTERNET\s+ETPRIME",
            r"ECONOMIC\s+TIMES\s+PRIME\s+SUB",
            r"UPI/CR/\d+/ETPRIME/AUTOPAY"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "care@economictimes.com",
        "grievance_email": "grievance@timesinternet.in",
        "cancellation_pitfall": "Annual AutoPay triggers 48h prior to expiration."
    },
    {
        "id": "apple_music",
        "name": "Apple Music Individual / Family",
        "category": "Music & Audio",
        "parent": "Apple Inc.",
        "parent_id": "apple",
        "official_website": "https://www.apple.com/in/apple-music",
        "logo": "https://cdn.simpleicons.org/applemusic/FA243C",
        "default_amount": 99.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"APPLE\.COM/BILL\s+APPLE\s+MUSIC",
            r"ITUNES\.COM/BILL\s+MUSIC",
            r"APPLE\s+MUSIC\s+RECURRING"
        ],
        "default_mechanism": "APP_STORE",
        "support_email": "appleid_iien@email.apple.com",
        "grievance_email": "grievance-officer-india@apple.com",
        "cancellation_pitfall": "Must cancel in Apple Settings > Apple ID > Subscriptions."
    },
    {
        "id": "apple_icloud",
        "name": "Apple iCloud+ Storage (50GB/200GB/2TB)",
        "category": "Cloud & Backup",
        "parent": "Apple Inc.",
        "parent_id": "apple",
        "official_website": "https://www.apple.com/in/icloud",
        "logo": "https://cdn.simpleicons.org/icloud/369BE9",
        "default_amount": 75.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"APPLE\.COM/BILL\s+ICLOUD",
            r"APPLE\s+ICLOUD\s+STORAGE\s+IN",
            r"ITUNES\.COM/BILL\s+ICLOUD\+"
        ],
        "default_mechanism": "APP_STORE",
        "support_email": "appleid_iien@email.apple.com",
        "grievance_email": "grievance-officer-india@apple.com",
        "cancellation_pitfall": "Downgrading below current stored quota will prevent new email reception and camera photo syncing."
    },
    {
        "id": "apple_one",
        "name": "Apple One Bundle",
        "category": "Ecosystem Bundle",
        "parent": "Apple Inc.",
        "parent_id": "apple",
        "official_website": "https://www.apple.com/in/apple-one",
        "logo": "https://cdn.simpleicons.org/apple/000000",
        "default_amount": 195.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"APPLE\.COM/BILL\s+APPLE\s+ONE",
            r"APPLE\s+ONE\s+SUBSCRIPTION\s+IN",
            r"ITUNES\.COM/BILL\s+APPLE\s+ONE"
        ],
        "default_mechanism": "APP_STORE",
        "support_email": "appleid_iien@email.apple.com",
        "grievance_email": "grievance-officer-india@apple.com",
        "cancellation_pitfall": "Cancelling cancels Apple Music, TV+, Arcade and iCloud simultaneously."
    },
    {
        "id": "claude_pro",
        "name": "Claude Pro (Anthropic)",
        "category": "AI & Technology",
        "parent": "Anthropic PBC",
        "parent_id": "anthropic",
        "official_website": "https://claude.ai",
        "logo": "https://cdn.simpleicons.org/anthropic/191919",
        "default_amount": 1999.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"ANTHROPIC\s+\*CLAUDE\s+PRO",
            r"ANTHROPIC\s+PBC\s+SAN\s+FRANCISCO",
            r"STRIPE\*ANTHROPIC\s+CLAUDE"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@anthropic.com",
        "grievance_email": "privacy@anthropic.com",
        "cancellation_pitfall": "Billed in USD ($20/mo + GST). Cancel in Claude.ai > Settings > Billing."
    },
    {
        "id": "perplexity_pro",
        "name": "Perplexity Pro AI",
        "category": "AI & Search",
        "parent": "Perplexity AI Inc.",
        "parent_id": "perplexity",
        "official_website": "https://www.perplexity.ai/pro",
        "logo": "https://cdn.simpleicons.org/perplexity/20B2AA",
        "default_amount": 1650.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"PERPLEXITY\s+AI\s+SAN\s+FRANCISCO",
            r"PERPLEXITY\*PRO\s+SUBSCRIPTION",
            r"STRIPE\*PERPLEXITY\s+AI"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@perplexity.ai",
        "grievance_email": "support@perplexity.ai",
        "cancellation_pitfall": "Often activated via Airtel or promotional codes; check source of subscription."
    },
    {
        "id": "midjourney",
        "name": "Midjourney AI",
        "category": "AI & Image Generation",
        "parent": "Midjourney Inc.",
        "parent_id": "midjourney",
        "official_website": "https://www.midjourney.com",
        "logo": "https://cdn.simpleicons.org/midjourney/000000",
        "default_amount": 830.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"MIDJOURNEY\s+INC\s+SAN\s+FRANCISCO",
            r"STRIPE\*MIDJOURNEY\s+SUBSCRIPTION",
            r"POS\s+DEBIT\s+MIDJOURNEY"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "billing@midjourney.com",
        "grievance_email": "billing@midjourney.com",
        "cancellation_pitfall": "Unused GPU fast hours expire upon monthly renewal."
    },
    {
        "id": "figma_pro",
        "name": "Figma Professional",
        "category": "Design & Prototyping",
        "parent": "Figma Inc.",
        "parent_id": "figma",
        "official_website": "https://www.figma.com/pricing",
        "logo": "https://cdn.simpleicons.org/figma/F24E1E",
        "default_amount": 1250.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"FIGMA\s+INC\s+SAN\s+FRANCISCO",
            r"FIGMA\*PRO\s+SUBSCRIPTION",
            r"STRIPE\*FIGMA\s+DESIGN"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@figma.com",
        "grievance_email": "support@figma.com",
        "cancellation_pitfall": "Adding a team editor silently adds ₹1,250/mo per extra seat without checkout prompt."
    },
    {
        "id": "slack_pro",
        "name": "Slack Pro (Salesforce)",
        "category": "Team Communication & SaaS",
        "parent": "Salesforce Inc.",
        "parent_id": "salesforce",
        "official_website": "https://slack.com",
        "logo": "https://cdn.simpleicons.org/slack/4A154B",
        "default_amount": 750.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"SLACK\s+TECHNOLOGIES\s+LTD\s+DUBLIN",
            r"SLACK\*PRO\s+SUBSCRIPTION",
            r"POS\s+DEBIT\s+SLACK\s+TECH"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "feedback@slack.com",
        "grievance_email": "privacy@salesforce.com",
        "cancellation_pitfall": "Fair billing policy applies credits for inactive users, but team downgrade requires admin."
    },
    {
        "id": "jira_software",
        "name": "Jira Software (Atlassian)",
        "category": "Project Management & SaaS",
        "parent": "Atlassian Corporation",
        "parent_id": "atlassian",
        "official_website": "https://www.atlassian.com/software/jira",
        "logo": "https://cdn.simpleicons.org/jira/0052CC",
        "default_amount": 650.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"ATLASSIAN\s+PTY\s+LTD\s+SYDNEY",
            r"ATLASSIAN\*JIRA\s+SUBSCRIPTION",
            r"POS\s+DEBIT\s+ATLASSIAN"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@atlassian.com",
        "grievance_email": "privacy@atlassian.com",
        "cancellation_pitfall": "Must unsubscribe from admin.atlassian.com under Subscriptions."
    },
    {
        "id": "trello_premium",
        "name": "Trello Premium (Atlassian)",
        "category": "Task Management",
        "parent": "Atlassian Corporation",
        "parent_id": "atlassian",
        "official_website": "https://trello.com",
        "logo": "https://cdn.simpleicons.org/trello/0052CC",
        "default_amount": 420.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"TRELLO\s+INC\s+NEW\s+YORK",
            r"ATLASSIAN\*TRELLO\s+SUB",
            r"POS\s+DEBIT\s+TRELLO"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@trello.com",
        "grievance_email": "privacy@atlassian.com",
        "cancellation_pitfall": "Workspaces revert to 10 boards limit."
    },
    {
        "id": "zoho_one",
        "name": "Zoho One / Zoho Books",
        "category": "Enterprise & Accounting",
        "parent": "Zoho Corporation",
        "parent_id": "zoho",
        "official_website": "https://www.zoho.com",
        "logo": "https://cdn.simpleicons.org/zoho/ED1C24",
        "default_amount": 1800.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"ZOHO\s+CORPORATION\s+PVT\s+LTD\s+CHENNAI",
            r"ZOHO\*BOOKS\s+SUBSCRIPTION",
            r"UPI/CR/\d+/ZOHO/RECURRING"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@zohocorp.com",
        "grievance_email": "privacy@zohocorp.com",
        "cancellation_pitfall": "Manage via payments.zoho.com."
    },
    {
        "id": "freshworks",
        "name": "Freshdesk / Freshworks",
        "category": "Customer Support & CRM",
        "parent": "Freshworks Inc.",
        "parent_id": "freshworks",
        "official_website": "https://www.freshworks.com",
        "logo": "https://cdn.simpleicons.org/freshworks/F15B2A",
        "default_amount": 1200.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"FRESHWORKS\s+INC\s+SAN\s+MATEO",
            r"FRESHDESK\s+SUBSCRIPTION\s+CHENNAI",
            r"POS\s+DEBIT\s+FRESHWORKS"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@freshworks.com",
        "grievance_email": "compliance@freshworks.com",
        "cancellation_pitfall": "Requires Account Owner permission to cancel plan."
    },
    {
        "id": "tata_neupass",
        "name": "Tata NeuPass",
        "category": "Retail & Lifestyle",
        "parent": "Tata Sons (Tata Digital)",
        "parent_id": "tata_group",
        "official_website": "https://www.tataneu.com",
        "logo": "https://cdn.simpleicons.org/tata/005A9C",
        "default_amount": 499.0,
        "supported_cadences": ["ANNUAL"],
        "descriptors": [
            r"TATA\s+DIGITAL\s+PVT\s+LTD\s+NEUPASS",
            r"TATA\s+NEU\s+MEMBERSHIP",
            r"UPI/CR/\d+/TATADIGITAL/NEUPASS"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@tataneu.com",
        "grievance_email": "grievance@tatadigital.com",
        "cancellation_pitfall": "Revoke mandate in UPI app."
    },
    {
        "id": "tata_1mg",
        "name": "Tata 1mg Care Plan",
        "category": "Healthcare & Pharmacy",
        "parent": "Tata Sons (Tata Digital)",
        "parent_id": "tata_group",
        "official_website": "https://www.1mg.com/careplan",
        "logo": "https://cdn.simpleicons.org/1mg/FF6F61",
        "default_amount": 199.0,
        "supported_cadences": ["QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"1MG\s+TECHNOLOGIES\s+PVT\s+LTD\s+CAREPLAN",
            r"TATA\s+1MG\s+CARE\s+PLAN",
            r"UPI/CR/\d+/1MG/CAREPLAN"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "care@1mg.com",
        "grievance_email": "grievance@1mg.com",
        "cancellation_pitfall": "Free lab test vouchers expire immediately upon plan end."
    },
    {
        "id": "apollo_circle",
        "name": "Apollo 24/7 Circle Membership",
        "category": "Healthcare & Wellness",
        "parent": "Apollo Hospitals Enterprise Ltd",
        "parent_id": "apollo_hospitals",
        "official_website": "https://www.apollo247.com/circle",
        "logo": "https://cdn.simpleicons.org/apollo/008899",
        "default_amount": 199.0,
        "supported_cadences": ["QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"APOLLO\s+247\s+HEALTH\s+CIRCLE",
            r"APOLLO\s+HOSPITALS\s+CIRCLE\s+MEM",
            r"UPI/CR/\d+/APOLLO/CIRCLE"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "helpdesk@apollo247.com",
        "grievance_email": "grievance@apollo247.com",
        "cancellation_pitfall": "Revoke AutoPay in your UPI App."
    },
    {
        "id": "pharmeasy_plus",
        "name": "PharmEasy Plus",
        "category": "Healthcare & Medicine",
        "parent": "API Holdings Ltd (PharmEasy)",
        "parent_id": "pharmeasy_corp",
        "official_website": "https://pharmeasy.in/plus",
        "logo": "https://cdn.simpleicons.org/pharmeasy/10847E",
        "default_amount": 199.0,
        "supported_cadences": ["QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"AXELIA\s+SOLUTIONS\s+PHARMEASY\s+PLUS",
            r"PHARMEASY\s+PLUS\s+SUBSCRIPTION",
            r"UPI/CR/\d+/PHARMEASY/PLUS"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "care@pharmeasy.in",
        "grievance_email": "grievanceofficer@pharmeasy.in",
        "cancellation_pitfall": "Axelia Solutions descriptor is often used on statements."
    },
    {
        "id": "cleartax",
        "name": "ClearTax TaxCloud / Filing Pro",
        "category": "Fintech & Taxes",
        "parent": "Defmacro Software Pvt Ltd (Clear)",
        "parent_id": "cleartax_corp",
        "official_website": "https://cleartax.in",
        "logo": "https://cdn.simpleicons.org/cleartax/3B71F3",
        "default_amount": 999.0,
        "supported_cadences": ["ANNUAL"],
        "descriptors": [
            r"DEFMACRO\s+SOFTWARE\s+PVT\s+LTD\s+CLEARTAX",
            r"CLEARTAX\s+PRO\s+ANNUAL\s+SUB",
            r"UPI/CR/\d+/CLEARTAX/MANDATE"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@cleartax.in",
        "grievance_email": "grievance@cleartax.in",
        "cancellation_pitfall": "Defmacro Software is the legal billing name."
    },
    {
        "id": "zerodha_kite_connect",
        "name": "Zerodha Kite Connect API",
        "category": "Trading & Investments",
        "parent": "Zerodha Broking Ltd",
        "parent_id": "zerodha",
        "official_website": "https://kite.trade",
        "logo": "https://cdn.simpleicons.org/zerodha/387ED1",
        "default_amount": 2000.0,
        "supported_cadences": ["MONTHLY"],
        "descriptors": [
            r"ZERODHA\s+BROKING\s+LTD\s+KITE\s+CONNECT",
            r"RAINMATTER\s+ZERODHA\s+API\s+SUB",
            r"POS\s+DEBIT\s+ZERODHA\s+KITE"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "talk@zerodha.com",
        "grievance_email": "grievances@zerodha.com",
        "cancellation_pitfall": "Requires disabling billing on developers.kite.trade console."
    },
    {
        "id": "moneycontrol_pro",
        "name": "Moneycontrol Pro",
        "category": "Financial Media & Markets",
        "parent": "Reliance Industries / Network18",
        "parent_id": "reliance_jio",
        "official_website": "https://www.moneycontrol.com/promos/pro.php",
        "logo": "https://cdn.simpleicons.org/moneycontrol/005A9C",
        "default_amount": 399.0,
        "supported_cadences": ["ANNUAL"],
        "descriptors": [
            r"EIGHTEEN\s+MEDIA\s+MONEYCONTROL\s+PRO",
            r"MONEYCONTROL\s+PRO\s+MEMBERSHIP",
            r"UPI/CR/\d+/MONEYCONTROL/PRO"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "pro@moneycontrol.com",
        "grievance_email": "grievanceofficer@nw18.com",
        "cancellation_pitfall": "Network18 / e-Eighteen Media descriptor appears on statement."
    },
    {
        "id": "tradingview_pro",
        "name": "TradingView Essential / Plus",
        "category": "Financial Markets & Charts",
        "parent": "TradingView Inc.",
        "parent_id": "tradingview",
        "official_website": "https://www.tradingview.com/gopro",
        "logo": "https://cdn.simpleicons.org/tradingview/2962FF",
        "default_amount": 1290.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"TRADINGVIEW\s+INC\s+OHIO",
            r"TRADINGVIEW\*SUBSCRIPTION",
            r"POS\s+DEBIT\s+TRADINGVIEW"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@tradingview.com",
        "grievance_email": "support@tradingview.com",
        "cancellation_pitfall": "Black Friday annual renewals charge at full non-discounted rate after year 1."
    },
    {
        "id": "the_ken",
        "name": "The Ken Subscription",
        "category": "Journalism & Business Media",
        "parent": "Ken Digital Media Pvt Ltd",
        "parent_id": "the_ken_corp",
        "official_website": "https://the-ken.com",
        "logo": "https://cdn.simpleicons.org/theken/C82333",
        "default_amount": 3250.0,
        "supported_cadences": ["ANNUAL"],
        "descriptors": [
            r"KEN\s+DIGITAL\s+MEDIA\s+PVT\s+LTD",
            r"THE\s+KEN\s+ANNUAL\s+SUBSCRIPTION",
            r"UPI/CR/\d+/THEKEN/MANDATE",
            r"ACH\s+D\s+KEN\s+DIGITAL\s+MEDIA"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "help@the-ken.com",
        "grievance_email": "grievance@the-ken.com",
        "cancellation_pitfall": "Annual AutoPay mandate must be revoked via UPI app before renewal cycle."
    },
    {
        "id": "the_morning_context",
        "name": "The Morning Context",
        "category": "Journalism & Business Media",
        "parent": "Slowform Media Pvt Ltd",
        "parent_id": "tmc_corp",
        "official_website": "https://themorningcontext.com",
        "logo": "https://cdn.simpleicons.org/tmc/000000",
        "default_amount": 2999.0,
        "supported_cadences": ["ANNUAL"],
        "descriptors": [
            r"SLOWFORM\s+MEDIA\s+PVT\s+LTD",
            r"THE\s+MORNING\s+CONTEXT\s+SUB",
            r"UPI/CR/\d+/MORNINGCONTEXT/SUB"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@themorningcontext.com",
        "grievance_email": "grievance@themorningcontext.com",
        "cancellation_pitfall": "Slowform Media is the corporate descriptor."
    },
    {
        "id": "coursera_plus",
        "name": "Coursera Plus",
        "category": "Education & Certifications",
        "parent": "Coursera Inc.",
        "parent_id": "coursera",
        "official_website": "https://www.coursera.org/courseraplus",
        "logo": "https://cdn.simpleicons.org/coursera/0056D2",
        "default_amount": 3500.0,
        "supported_cadences": ["ANNUAL", "MONTHLY"],
        "descriptors": [
            r"COURSERA\s+INC\s+MOUNTAIN\s+VIEW",
            r"COURSERA\*PLUS\s+SUBSCRIPTION",
            r"POS\s+DEBIT\s+COURSERA"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@coursera.org",
        "grievance_email": "privacy@coursera.org",
        "cancellation_pitfall": "Certificates earned remain valid; course access expires upon plan termination."
    },
    {
        "id": "leetcode_premium",
        "name": "LeetCode Premium",
        "category": "Developer & Interview Prep",
        "parent": "LeetCode LLC",
        "parent_id": "leetcode",
        "official_website": "https://leetcode.com/subscribe",
        "logo": "https://cdn.simpleicons.org/leetcode/FFA116",
        "default_amount": 2999.0,
        "supported_cadences": ["ANNUAL", "MONTHLY"],
        "descriptors": [
            r"LEETCODE\s+LLC\s+PALO\s+ALTO",
            r"LEETCODE\*PREMIUM\s+SUBSCRIPTION",
            r"STRIPE\*LEETCODE"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "billing@leetcode.com",
        "grievance_email": "support@leetcode.com",
        "cancellation_pitfall": "Company tagged problem lists revert to locked upon cycle end."
    },
    {
        "id": "dropbox_plus",
        "name": "Dropbox Plus (2TB)",
        "category": "Cloud & Backup",
        "parent": "Dropbox Inc.",
        "parent_id": "dropbox",
        "official_website": "https://www.dropbox.com/plans",
        "logo": "https://cdn.simpleicons.org/dropbox/0061FF",
        "default_amount": 830.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"DROPBOX\s+\*[0-9A-Z]+\s+SAN\s+FRANCISCO",
            r"DROPBOX\s+INC\s+SUBSCRIPTION",
            r"POS\s+DEBIT\s+DROPBOX"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@dropbox.com",
        "grievance_email": "privacy@dropbox.com",
        "cancellation_pitfall": "Files above 2GB remain stored but syncing halts."
    },
    {
        "id": "proton_unlimited",
        "name": "Proton Unlimited / Mail",
        "category": "Privacy & Security",
        "parent": "Proton AG",
        "parent_id": "proton",
        "official_website": "https://proton.me",
        "logo": "https://cdn.simpleicons.org/protonmail/6D4AFF",
        "default_amount": 850.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"PROTON\s+AG\s+GENEVA\s+SWITZERLAND",
            r"PROTON\*UNLIMITED\s+SUBSCRIPTION",
            r"POS\s+DEBIT\s+PROTON\s+AG"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "support@proton.me",
        "grievance_email": "privacy@proton.me",
        "cancellation_pitfall": "Downgrade requires disabling extra custom domain email addresses."
    },
    {
        "id": "medium_membership",
        "name": "Medium Membership",
        "category": "Publishing & Media",
        "parent": "A Medium Corporation",
        "parent_id": "medium_corp",
        "official_website": "https://medium.com/membership",
        "logo": "https://cdn.simpleicons.org/medium/000000",
        "default_amount": 420.0,
        "supported_cadences": ["MONTHLY", "ANNUAL"],
        "descriptors": [
            r"MEDIUM\s+CORP\s+SAN\s+FRANCISCO",
            r"MEDIUM\*MEMBERSHIP\s+RECURRING",
            r"STRIPE\*MEDIUM\s+CORP"
        ],
        "default_mechanism": "CARD_SI",
        "support_email": "yourfriends@medium.com",
        "grievance_email": "privacy@medium.com",
        "cancellation_pitfall": "Cancel via medium.com/me/settings/membership."
    },
    {
        "id": "fittr_coach",
        "name": "Fittr Coaching Subscription",
        "category": "Fitness & Nutrition",
        "parent": "Squats Fitness Pvt Ltd (Fittr)",
        "parent_id": "fittr_corp",
        "official_website": "https://www.fittr.com",
        "logo": "https://cdn.simpleicons.org/fitbit/00B0B9",
        "default_amount": 2500.0,
        "supported_cadences": ["QUARTERLY", "ANNUAL"],
        "descriptors": [
            r"SQUATS\s+FITNESS\s+PVT\s+LTD\s+PUNE",
            r"FITTR\s+COACHING\s+RECURRING",
            r"UPI/CR/\d+/FITTR/MANDATE"
        ],
        "default_mechanism": "UPI_AUTOPAY",
        "support_email": "support@fittr.com",
        "grievance_email": "grievance@fittr.com",
        "cancellation_pitfall": "Squats Fitness Pvt Ltd is the billing descriptor."
    }
]

# Parent corporate mapping
PARENT_COMPANIES = {
    "alphabet": {
        "id": "alphabet",
        "name": "Alphabet Inc.",
        "ticker": "NASDAQ: GOOGL",
        "country": "United States",
        "headquarters": "Mountain View, California",
        "description": "Parent conglomerate of Google, YouTube, Android, DeepMind, Waymo.",
        "shared_account_portal": "https://myaccount.google.com/payments-and-subscriptions"
    },
    "amazon": {
        "id": "amazon",
        "name": "Amazon.com Inc.",
        "ticker": "NASDAQ: AMZN",
        "country": "United States",
        "headquarters": "Seattle, Washington",
        "description": "Global e-commerce and cloud giant owning Prime, AWS, Audible, Twitch, MGM.",
        "shared_account_portal": "https://www.amazon.in/mc/manage"
    },
    "microsoft": {
        "id": "microsoft",
        "name": "Microsoft Corporation",
        "ticker": "NASDAQ: MSFT",
        "country": "United States",
        "headquarters": "Redmond, Washington",
        "description": "Tech giant owning Windows, Office 365, Azure, Xbox, LinkedIn, GitHub.",
        "shared_account_portal": "https://account.microsoft.com/services"
    },
    "apple": {
        "id": "apple",
        "name": "Apple Inc.",
        "ticker": "NASDAQ: AAPL",
        "country": "United States",
        "headquarters": "Cupertino, California",
        "description": "Hardware and digital services provider operating iCloud, Apple Music, App Store.",
        "shared_account_portal": "https://reportaproblem.apple.com"
    },
    "netflix": {
        "id": "netflix",
        "name": "Netflix Inc.",
        "ticker": "NASDAQ: NFLX",
        "country": "United States",
        "headquarters": "Los Gatos, California",
        "description": "Global streaming entertainment subscription service.",
        "shared_account_portal": "https://www.netflix.com/youraccount"
    },
    "spotify": {
        "id": "spotify",
        "name": "Spotify Technology S.A.",
        "ticker": "NYSE: SPOT",
        "country": "Sweden",
        "headquarters": "Stockholm, Sweden",
        "description": "Leading global audio and podcast streaming provider.",
        "shared_account_portal": "https://www.spotify.com/account/overview"
    },
    "disney": {
        "id": "disney",
        "name": "The Walt Disney Company",
        "ticker": "NYSE: DIS",
        "country": "United States",
        "headquarters": "Burbank, California",
        "description": "Media giant owning Disney+, Hotstar, Marvel, Star Wars, ESPN, ABC.",
        "shared_account_portal": "https://www.hotstar.com/in/my-account"
    },
    "swiggy_corp": {
        "id": "swiggy_corp",
        "name": "Bundl Technologies Pvt Ltd (Swiggy)",
        "ticker": "NSE: SWIGGY",
        "country": "India",
        "headquarters": "Bengaluru, Karnataka",
        "description": "Indian on-demand convenience platform operating Swiggy Food, Instamart, Dineout.",
        "shared_account_portal": "https://www.swiggy.com/my-account"
    },
    "zomato_corp": {
        "id": "zomato_corp",
        "name": "Eternal Limited (Zomato Ltd)",
        "ticker": "NSE: ZOMATO",
        "country": "India",
        "headquarters": "Gurugram, Haryana",
        "description": "Indian food tech, dining and quick-commerce company operating Zomato and Blinkit.",
        "shared_account_portal": "https://www.zomato.com/gold"
    },
    "curefit": {
        "id": "curefit",
        "name": "Curefit Healthcare Pvt Ltd",
        "ticker": "Private",
        "country": "India",
        "headquarters": "Bengaluru, Karnataka",
        "description": "Health and fitness fitness ecosystem operating Cult.fit and Cultpass.",
        "shared_account_portal": "https://www.cult.fit/profile/memberships"
    },
    "times_group": {
        "id": "times_group",
        "name": "Times Internet (Bennett Coleman)",
        "ticker": "Private",
        "country": "India",
        "headquarters": "Noida, Uttar Pradesh",
        "description": "India's largest digital media network operating Times Prime, Gaana, ET.",
        "shared_account_portal": "https://www.timesprime.com/profile"
    },
    "reliance_jio": {
        "id": "reliance_jio",
        "name": "Reliance Industries / Jio Platforms",
        "ticker": "NSE: RELIANCE",
        "country": "India",
        "headquarters": "Mumbai, Maharashtra",
        "description": "India's largest telecommunications and media conglomerate (JioCinema, Viacom18).",
        "shared_account_portal": "https://www.jiocinema.com"
    },
    "airtel": {
        "id": "airtel",
        "name": "Bharti Airtel Limited",
        "ticker": "NSE: BHARTIARTL",
        "country": "India",
        "headquarters": "New Delhi, India",
        "description": "Multinational telecom service provider offering Airtel Xstream and connectivity.",
        "shared_account_portal": "https://www.airtel.in"
    },
    "tata_group": {
        "id": "tata_group",
        "name": "Tata Sons (Tata Play / Tata Neu)",
        "ticker": "Private / Conglomerate",
        "country": "India",
        "headquarters": "Mumbai, Maharashtra",
        "description": "Historic Indian multinational conglomerate operating Tata Play Binge and Tata Neu.",
        "shared_account_portal": "https://www.tataplay.com"
    },
    "adobe": {
        "id": "adobe",
        "name": "Adobe Inc.",
        "ticker": "NASDAQ: ADBE",
        "country": "United States",
        "headquarters": "San Jose, California",
        "description": "Global leader in digital creative tools, PDF Acrobat, Photoshop and marketing software.",
        "shared_account_portal": "https://account.adobe.com/plans"
    },
    "canva": {
        "id": "canva",
        "name": "Canva Pty Ltd",
        "ticker": "Private",
        "country": "Australia",
        "headquarters": "Surry Hills, Sydney",
        "description": "Global visual communications and graphic design platform.",
        "shared_account_portal": "https://www.canva.com/settings/billing"
    },
    "notion": {
        "id": "notion",
        "name": "Notion Labs Inc.",
        "ticker": "Private",
        "country": "United States",
        "headquarters": "San Francisco, California",
        "description": "Connected workspace for notes, wiki, projects and team documents.",
        "shared_account_portal": "https://www.notion.so/settings"
    },
    "openai": {
        "id": "openai",
        "name": "OpenAI LLC",
        "ticker": "Private",
        "country": "United States",
        "headquarters": "San Francisco, California",
        "description": "Artificial intelligence research and deployment company behind ChatGPT.",
        "shared_account_portal": "https://chatgpt.com"
    },
    "icici_group": {
        "id": "icici_group",
        "name": "ICICI Bank Group",
        "ticker": "NSE: ICICIBANK",
        "country": "India",
        "headquarters": "Mumbai, Maharashtra",
        "description": "Leading Indian private banking and insurance financial group.",
        "shared_account_portal": "https://www.icicibank.com"
    },
    "hdfc_group": {
        "id": "hdfc_group",
        "name": "HDFC Bank Group",
        "ticker": "NSE: HDFCBANK",
        "country": "India",
        "headquarters": "Mumbai, Maharashtra",
        "description": "India's largest private sector bank and financial services conglomerate.",
        "shared_account_portal": "https://www.hdfcbank.com"
    },
    "bajaj_group": {
        "id": "bajaj_group",
        "name": "Bajaj Finserv Ltd",
        "ticker": "NSE: BAJAJFINSV",
        "country": "India",
        "headquarters": "Pune, Maharashtra",
        "description": "Indian non-banking financial services company offering consumer financing and EMIs.",
        "shared_account_portal": "https://www.bajajfinserv.in"
    }
}

# Payment Mechanisms and their formal RBI / CCPA Cancellation Workflows
PAYMENT_MECHANISMS = {
    "UPI_AUTOPAY": {
        "name": "UPI AutoPay",
        "code": "UPI_AUTOPAY",
        "description": "NPCI UPI recurring mandate authenticated via UPI PIN.",
        "authority": "National Payments Corporation of India (NPCI) & RBI",
        "cancellation_steps": [
            "Open your primary UPI App (Google Pay, PhonePe, Paytm, BHIM, or Bank UPI App).",
            "Go to Profile or Settings > 'Autopay' / 'Mandates' / 'Automatic Payments'.",
            "Find the active mandate under the merchant's name.",
            "Tap 'Pause' or 'Revoke Mandate' / 'Cancel Autopay'.",
            "Enter your UPI PIN to authenticate cancellation. Ensure status changes to 'Revoked'."
        ],
        "turnaround_time": "Immediate (instant revocation in NPCI central switch)",
        "legal_backing": "RBI Circular DPSS.CO.PD.No.S513/02.14.003/2021-22: Mandate cancellation requests must be executed without undue delay and confirmation shared with customer."
    },
    "CARD_SI": {
        "name": "Card Standing Instruction (e-Mandate)",
        "code": "CARD_SI",
        "description": "Recurring e-mandate registered on Debit/Credit card with AFA (Additional Factor Authentication).",
        "authority": "Reserve Bank of India (RBI) e-Mandate Framework",
        "cancellation_steps": [
            "Log in to the Merchant's billing settings and select 'Cancel Subscription'.",
            "Crucial step: Log in to your Issuing Bank's NetBanking or Mobile App.",
            "Navigate to 'Cards' > 'Card Services' > 'Manage Standing Instructions' or 'e-Mandates'.",
            "Locate the merchant name and click 'Modify / Revoke Mandate'.",
            "Alternatively, use your bank's SI Hub portal (e.g. SIHub by BillDesk / PayU) to remove authorization."
        ],
        "turnaround_time": "1-2 business days for bank-side synchronization",
        "legal_backing": "RBI Circular RBI/2020-21/74: The issuer bank must provide a web portal / mobile dashboard allowing the cardholder to view, modify, or revoke any standing instruction at any time without fee."
    },
    "BANK_NACH": {
        "name": "Bank NACH / eNACH Mandate",
        "code": "BANK_NACH",
        "description": "National Automated Clearing House direct bank account debit mandate.",
        "authority": "NPCI NACH Division & RBI Banking Regulation Act",
        "cancellation_steps": [
            "Submit a formal written or email cancellation notice to the Merchant (retain copy of email).",
            "Log into your Bank's NetBanking portal and go to 'eNACH Mandates' or 'ECS / NACH Services'.",
            "Select the UMRN (Unique Mandate Reference Number) and click 'Stop / Cancel Mandate'.",
            "If your bank portal lacks self-service NACH cancellation, download the bank's Mandate Revocation Form and submit it to your home branch with the merchant acknowledgement."
        ],
        "turnaround_time": "3-5 banking days",
        "legal_backing": "NPCI Procedural Guidelines on NACH Mandates: The destination bank is legally obligated to register customer stop-payment or revocation request upon receipt of valid instruction."
    },
    "PLAY_STORE": {
        "name": "Google Play Store Subscriptions",
        "code": "PLAY_STORE",
        "description": "Subscription billed through Google Play In-App Billing on Android devices.",
        "authority": "Google Payments / Play Store Terms of Service",
        "cancellation_steps": [
            "Open Google Play Store on your Android device or visit play.google.com/store/account/subscriptions.",
            "Tap on your profile icon at top-right > 'Payments & subscriptions' > 'Subscriptions'.",
            "Select the subscription you want to cancel.",
            "Tap 'Cancel subscription' at the bottom.",
            "Select a cancellation reason and tap 'Continue' to confirm."
        ],
        "turnaround_time": "Immediate confirmation via email",
        "legal_backing": "CCPA Guidelines for Prevention and Regulation of Dark Patterns 2023: Subscriptions must provide cancellation in as few or fewer clicks than registration."
    },
    "APP_STORE": {
        "name": "Apple App Store Subscriptions",
        "code": "APP_STORE",
        "description": "Subscription billed through Apple In-App Purchases on iOS / iPadOS / macOS.",
        "authority": "Apple Media Services Terms and Conditions",
        "cancellation_steps": [
            "Open 'Settings' on your iPhone / iPad.",
            "Tap your Name / Apple ID banner at the top.",
            "Tap 'Subscriptions'.",
            "Tap the subscription you want to manage.",
            "Tap 'Cancel Subscription' (or 'Cancel Free Trial') and confirm."
        ],
        "turnaround_time": "Immediate confirmation via Apple ID email",
        "legal_backing": "CCPA / Consumer Protection Act 2019: Deceptive subscription barriers prohibited."
    },
    "DIRECT_MERCHANT": {
        "name": "Direct Merchant Billing (SaaS / Web Portal)",
        "code": "DIRECT_MERCHANT",
        "description": "Direct recurring credit card or payment gateway subscription on merchant website.",
        "authority": "Consumer Protection Act, 2019 (CCPA)",
        "cancellation_steps": [
            "Sign in to the merchant's official portal and navigate to 'Account Settings' > 'Billing' or 'Membership'.",
            "Click 'Cancel Subscription' or 'Turn Off Auto-Renew'.",
            "Save the cancellation confirmation screen and receipt email.",
            "If the merchant does not provide a cancellation button, send a formal written notice to their registered customer support and Grievance Officer."
        ],
        "turnaround_time": "Instant on portal or 48 hours via email",
        "legal_backing": "Consumer Protection (E-Commerce) Rules, 2020: Every e-commerce entity must acknowledge cancellation notices within 48 hours and process redressal within 30 days."
    }
}

# The 4-Tier Legal Escalation Chain if Merchant or Bank Fails to Cancel
ESCALATION_CHAIN = [
    {
        "tier": 1,
        "name": "Merchant Written Notice & Audit Trail",
        "target": "Merchant Support & India Grievance Officer",
        "sla": "48 Hours to Acknowledge, 7 Days to Rectify",
        "summary": "Send formal email quoting the Mandate / UMRN / Card Reference, specifying revocation of consent under Consumer Protection Rules 2020.",
        "action": "Use Mandate Radar's generated cancellation email to establish an unassailable legal paper trail."
    },
    {
        "tier": 2,
        "name": "Bank Dispute & Chargeback Request",
        "target": "Issuing Bank / Card Operations Division",
        "sla": "Chargeback Lodged within 14 Days",
        "summary": "Under RBI e-mandate master instructions, if debits continue after mandate revocation, the issuing bank must reverse the unauthorized debit.",
        "action": "Submit bank dispute form attaching Tier 1 cancellation proof and statement snippet."
    },
    {
        "tier": 3,
        "name": "Reserve Bank of India (RBI CMS)",
        "target": "RBI Integrated Ombudsman Scheme (cms.rbi.org.in)",
        "sla": "30 Days Resolution",
        "summary": "File complaint on the RBI Complaint Management System (CMS) against the bank if unrevoked auto-debits were processed or bank refused to block standing instruction.",
        "action": "Lodge online complaint at https://cms.rbi.org.in or email crpc@rbi.org.in."
    },
    {
        "tier": 4,
        "name": "National Consumer Helpline & CCPA",
        "target": "Ministry of Consumer Affairs (NCH 1915)",
        "sla": "Formal Consumer Grievance Registration",
        "summary": "National Consumer Helpline (NCH) toll-free 1915 / consumerhelpline.gov.in for unfair trade practice and dark patterns (Obstruction / Forced Continuity).",
        "action": "Call 1915 or lodge docket on consumerhelpline.gov.in quoting Merchant's corporate PAN/CIN."
    }
]

# Hard negative rules for non-mandates that must be safely filtered out:
HARD_NEGATIVE_PATTERNS = [
    {
        "category": "Weekly Groceries",
        "descriptors": [r"ZEPTO\s+CONSUMER", r"BLINKIT\s+COMMERCE", r"INSTAMART\s+BUNDL", r"BIGBASKET\s+DAILY"],
        "reason": "Variable weekly grocery purchases are discretionary grocery orders, not fixed-term subscriptions or auto-debit mandates."
    },
    {
        "category": "Fluctuating Utilities",
        "descriptors": [r"BESCOM\s+BANGALORE", r"ADANI\s+ELECTRICITY", r"TATA\s+POWER\s+MUMBAI", r"IGL\s+GAS\s+BILL"],
        "reason": "Utility bills fluctuate in consumption every month (>3% variations across multiple cycles) and are metered usage rather than fixed commitment mandates."
    },
    {
        "category": "Discretionary Food Deliveries",
        "descriptors": [r"SWIGGY\s+FOOD\s+DELIVERY", r"ZOMATO\s+RESTAURANT\s+ORDER", r"DOMINOS\s+PIZZA\s+ONLINE"],
        "reason": "Discretionary ad-hoc food delivery orders with unpredictable intervals (e.g. 2-5 days apart) rather than synchronized recurring cycles."
    }
]
