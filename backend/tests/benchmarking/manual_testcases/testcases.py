TEST_CASES_BERTSCORE = [
    ("We may collect information about your location and device usage to enhance your experience.",
    "The service provider may collect your location data to improve your experience, but they may also use this information for other purposes like targeted ads."),
    
    ("By using our service, you grant us a worldwide, non-exclusive, royalty-free license to use, reproduce, and distribute your user-generated content.",
    "This service can use and share you content worldwide without paying you, which may raise concerns about ownership and compensation."),
    
    ("We reserve the right to terminate your account at any time for any reason without notice.",
    "The company has the power to end you account without notice or explanation, which could ead to loss of access and data."),
    
    ("Your personal information may be shared with our affiliates and partners for marketing purposes.",
    "Your data may be used for targeted ads, potentially without your direct consent, and shared with unknown third parties."),
    
    ("We may modify these terms at any time, and your continued use of the service constitutes acceptance of the changes.",
    "This means the compnay can change its rules without your explicit consent, and contued use implies agreement to new terms."),
    
    ("In the event of a dispute, you agree to resolve the issue through binding arbitration rather than in court.",
    "You may be giving up your right to a court trial if a dispute arises, and instead, a neutral third party will make a decision."),
    
    ("We use cookies and similar technologies to track your activity on our site and other sites.",
    "The company uses technologies to monitor what you do on their site and potentially on other websites too. This extensive tracking could raise privacy concerns."),
    
    ("You are responsible for maintaining the confidentiality of your account information and password.",
    "You need to keep your account details and password secret. While this is standard, it means the company might not help you if your account is compromised due to your own negligence."),
    
    ("We may use your name and profile picture in connection with commercial or sponsored content.",
    "The company might use your name and picture for ads or sponsored posts. This could mean your identity is used to promote products or services without your explicit consent for each use."),
    
    ("By submitting ideas or feedback, you grant us the right to use them without compensation or attribution.",
    "If you give the company ideas or feedback, they can use them for free without giving you credit or payment. This means you could potentially lose out on valuable ideas you share."),
    
    ("All of Your uses of the Netflix Brand Assets in any of Your marketing, advertising, content, or other material (""Your Materials"") are subject to Netflix's approval prior to use.",
        "You must ask permission and get the consent of Netflix before using any of their assets and branding in your marketing or content. This could limit your creative freedom and require extra steps before you can use their materials."),
    
    ("You acknowledge and agree to provide public-facing contact information, a refund policy and order fulfilment timelines on your Shopify Store.", 
        "This company requires you to share your contact details and refund policy on your Shopify store."),
]

TEST_CASES_CLASSIFICATION = [
    ("We may collect information about your location and device usage to enhance your experience.", 'First Party Collection/Use'),
    
    ("Your data will be retained for as long as necessary to provide you with our services.", 'Data Retention'),
    
    ("If you have any questions about our privacy practices, you can contact us at privacy@example.com.", 'Privacy contact information'),
    
    ("Our service is not intended for use by children under the age of 13.", 'International and Specific Audiences'),
    
    ("We have implemented industry-standard security measures to protect your personal information.", 'Data Security'),
    
    ("Users can request access to, edit, or delete their personal information through their account settings.", 'User Access, Edit and Deletion'),
    
    ("By using our service, you agree to the terms and conditions outlined in this agreement.", 'Introductory/Generic'),
    
    ("You have the option to opt-out of certain data collection practices at any time.", 'User Choice/Control'),
]