LADOKE AKINTOLA UNIVERSITY OF TECHNOLOGY
Department of Computer Science
FINAL YEAR PROJECT 
DESIGN AND IMPLEMENTATION OF LIBRARY MANAGEMENT SYSTEM USING NASAL AND THUMBRINT BIOMETRICS
BY
ADESANWO JOSHUA OLUSEGUN(2021000382)
&
ABUBAKAR ABDULLAH ISHAQ(2021002417)
IN PARTIAL FULFILMENT OF THE REQUIREMENTS FOR THE AWARD OF THE BACHELOR OF TECHNOLOGY (B.TECH) IN COMPUTER SCIENCE

SUPERVISOR : PROF. W.O ISMAILA

CERTIFICATION
This is to certify that this report was carried out by ADESANWO JOSHUA OLUSEGUN (Matric Number 2021000382) and ABUBAKAR ABDULLAH ISHAQ (Matric Number 2021002417) and as part of the requirements for the award of Bachelor of Technology in the department of Computer Science, Faculty of Computing and Informatics, Ladoke Akintola University of Technology, Ogbomoso, Nigeria. 

........................................			                            ............................................	     HOD(PROF. ISMAILA )					               SUPERVISOR 
				
............................................... 			                     ......................................
       Date								    Date


DEDICATION
This project work is dedicated to almighty God, the author and finisher who kept us through our journey in this institution, gave us support, strength, wisdom, understanding in all areas.













ACKNOWLEDGEMENT
All appreciation and adorations are due to Almighty God, the Lord of all creations. Our immense gratitude to our family and friends for all their contribution, support, advice and encouragement. 
We greatly acknowledge the effort and contribution of our supervisor, Prof. W. O. ISMAILA, for his guidance and scolding which boosted our energy to ensure that we perfected the course of study during the project work. We also wish to acknowledge the effort of the staff of Computer Science Department of Ladoke Akintola University of Technology
We wish to express our profound gratitude to our parents and guardians for their unwavering financial support, moral guidance, and tireless prayers throughout our academic journey. Their sacrifices and constant encouragement have been the cornerstone of our success, providing the stability and motivation necessary to complete this project and our degree program.







ABSTRACT
The management of academic library resources has historically depended on manual data entry and token-based identification, which are highly susceptible to human error, unauthorized access, and administrative bottlenecks. While single-modality biometric systems, such as standalone fingerprint scanners, offer improved security over traditional library cards, they remain vulnerable to temporary physical injuries, environmental conditions, and sophisticated spoofing attempts. To address these persistent limitations, this study presents the design and implementation of a Multimodal Biometric Library Management System that integrates both nose-tip landmarks and thumbprint recognition. The primary aim of this system is to provide a tamper-proof, dual-layer authentication gateway with enhanced "liveness" detection to secure academic library resources.
The technical implementation utilized a Python backend, specifically leveraging the Django framework as the core Database Management System (DBMS), to securely manage student registrations, book issuance, and borrowing history without storing raw image files. To build a comprehensive training and testing dataset, concurrent multimodal samples were collected from 50 subjects within the LAUTECH community. The system's biometric pipeline employed OpenCV for rigorous image pre-processing, utilizing adaptive histogram equalization and grayscale conversion to ensure mathematical integrity. For feature extraction, Google's MediaPipe framework was deployed to map the rigid, spatial coordinates of the nasal geometry, while Independent Component Analysis (ICA) was implemented to isolate non-overlapping, independent thumbprint signatures.
Finally, the k-Nearest Neighbors (k-NN) classification algorithm was utilized to facilitate rapid, multi-class user matching against the central database. The system's reliability was benchmarked using standard performance metrics, including Overall Accuracy, False Positive Rate (FPR), Sensitivity, Specificity, and Average Computational Time. Ultimately, the fusion of non-contact nasal geometry with friction-ridge analysis effectively mitigates the false rejection rates inherent in standalone sensors, establishing a highly secure, efficient, and accessible solution for modern library administration.

TABLE OF CONTENT
CERTIFICATION	i
DEDICATION	ii
ACKNOWLEDGEMENT	iii
ABSTRACT	iv
CHAPTER 1: INTRODUCTION	1
1.1 INTRODUCTION	1
1.2 STATEMENT OF PROBLEM	2
1.3 AIM AND OBJECTIVES	3
1.4 SCOPE OF STUDY	4
1.5 LIMITATION OF STUDY	4
1.6 OPERATIONAL DEFINITION OF TERMS	5
CHAPTER 2: LITERATURE REVIEW	8
2.1 OVERVIEW OF MULTIMODAL BIOMETRIC LIBRARY SYSTEM	8
2.2 WHAT IS BIOMETRICS	8
2.3 HISTORY OF BIOMETRICS	9
2.4 OTHER APPLICATIONS OF BIOMETRICS	12
2.5 ANATOMICAL PATTERNS OF FINGERPRINTS	14
2.6 MICROSCOPIC MINUTIAE CHARACTERISTIC	15
2.7 FINGERPRINT SCANNER	16
2.8.1 FINGERPRINT AUTHENTICATION SYSTEMS	17
2.8.2 CONVERSION OF FINGERPRINT INTO GREYSCALE	18
2.8.3 NORMALIZATION OF FINGERPRINT	18
2.9 NOSE AND FACIAL LANDMARK BIOMETRICS	19
2.10 FEATURE EXTRACTION	20
2.11 INDEPENDENT COMPONENT ANALYSIS (ICA)	21
2.12 THE CLASSIFICATION PHASE	23
2.13 K-NEAREST NEIGHBORS (K-NN)	24
2.14 PERFORMANCE METRICS	25
CHAPTER 3: METHODOLOGY	31
3.1 METHODOLOGY	31
3.2 STAGES OF THE MULTIMODAL SYSTEM DEVELOPMENT	32
3.3 BIOMETRIC IMAGE ACQUISITION	32
3.4. BIOMETRIC IMAGE PRE-PROCESSING UTILIZING OPENCV	32
3.4.1 CONTRAST ADJUSTMENT	33
3.4.2 Image Conversion from RGB to HSV and YCbCr	34
3.5.1 CONTRAST ADJUSTMENT AND NOISE REDUCTION	35
3.6 FEATURE EXTRACTION USING MEDIAPIPE AND ICA	36
3.6.1 NASAL LANDMARK EXTRACTION VIA MEDIAPIPE	36
3.6.2 THUMPRINT LANDMARK EXTRACTION VIA MEDIAPIPE	37
3.7 CLASSIFICATION USING KNN (K NEAREST NEIGHBORS)	38
3.8 PERFORMANCE MEASURES OF THE DEVELOPED SYSTEM	40
REFERENCES	41




CHAPTER 1
1.1 INTRODUCTION
In the current decade, academic institutions are increasingly diverting from traditional, manual methods of managing library resources. Historically, library management has depended on manual data entry for user registration and book transactions, a process that is often time-consuming, labor-intensive, and susceptible to human error (Adeoti-Adekeye, 1997). Furthermore, manual systems face security risks such as unauthorized access, theft of materials, and inaccurate record-keeping.
To address these challenges, biometric technologies have emerged as a robust solution by providing non-replicable identification based on unique physiological traits. Research has definitively shown that biometric systems offer an inherently higher level of security than token-based or knowledge-based methods like passwords (Jain, Ross, & Prabhakar, 2004). While single-modality systems, such as fingerprint recognition, offer significant improvements in security and efficiency over traditional library cards or passwords, they are not without limitations. Factors such as physical injuries, environmental conditions, or sophisticated spoofing attempts can occasionally compromise the reliability of a single-biometric system (Maltoni et al., 2009).
This study proposes an advanced approach by developing a multimodal biometric library management system. By integrating both nose recognition (facial landmarks) and thumbprint verification, the system aims to provide a higher tier of security and "liveness" detection. Fusing multiple biological traits mathematically mitigates the failure rates of standalone biometric sensors (Ross, Nandakumar, & Jain, 2006). This dual-layer authentication ensures that only authorized individuals can access library resources, effectively streamlining operations while minimizing the risks associated with single-point biometric failures.



1.2 STATEMENT OF PROBLEM
The persistent reliance on manual or single-factor authentication systems in modern libraries introduces a multifaceted set of challenges that compromise administrative integrity and student satisfaction. One of the most glaring issues is the difficulty inherent in accurately tracking high-volume inventories and borrowing histories. Manual tracking leads to a compromised catalog, where misplaced items or unrecorded returns result in resource scarcity and administrative disputes (Oloyede & Alaya, 2013). Such labor-intensive processes not only consume valuable staff hours but also erode the trust between the library and its patrons when inaccuracies in due dates or fines arise.
Furthermore, single-modality biometric systems have revealed specific vulnerabilities. Fingerprint sensors can be impacted by temporary injuries like cuts or burns, or by the presence of dust and sweat, which can lead to legitimate students being rejected by the system (Jain et al., 2004). Additionally, most entry-level scanners lack the ability to distinguish between a live finger and an artificial duplicate, posing a persistent security threat. Advanced anti-spoofing measures are increasingly necessary to combat fraudulent biometric replicas (Marcel, Nixon, & Li, 2014).
The administrative burden of managing these failures often leads to "bottlenecks" during peak library hours, causing burnout among staff and frustration for students. There is, therefore, a critical need for a more secure, reliable, and efficient system that utilizes a dual-biometric approach combining the unique landmarks of the nose with the ridge patterns of the thumb to provide a tamper-proof, error-resistant solution for library resource management.
1.3 AIM AND OBJECTIVES
The primary aim of this research is to design and implement a Multimodal Biometric Library Management System that utilizes nose-tip landmarks and thumbprint recognition to automate user verification and resource tracking. By fusing two distinct biometric modalities, the system seeks to overcome the limitations of single-trait systems and provide a more secure, "liveness-tested" gateway for academic libraries.
In order to achieve this aim, the following specific objectives will be pursued
To architect a dual-acquisition system capable of capturing high-resolution thumbprint images through an optical scanner and facial nose landmarks via a digital camera
To develop a pre-processing pipeline involving image normalization, noise reduction, and grayscale conversion to ensure biometric data integrity
To implement Independent Component Analysis (ICA) as a robust feature extraction technique to isolate unique, non-overlapping biometric signatures from both the nose and thumb data
To deploy a k-Nearest Neighbors (k-NN) classification algorithm to facilitate rapid and accurate user matching within the central library database
To develop the system backend using Python (leveraging the Django framework) and a responsive frontend to manage student registration, book issuance, and borrowing history
To evaluate the system's performance using metrics such as Accuracy, False Positive Rate (FPR), Sensitivity, and Specificity to benchmark its reliability against traditional single-biometric models


1.4 SCOPE OF STUDY
The scope of this research is focused on the development of a biometric-led library management solution specifically tailored for the LAUTECH community. Data collection will involve 50 subjects, with multiple samples of nose-tip landmarks and thumbprints captured to build a comprehensive training and testing dataset. The technical implementation will utilize Python for its superior computer vision libraries, while the database will store biometric hashes rather than raw images to ensure user privacy. Performance evaluation will be strictly limited to the simulation of a local library environment, focusing on recognition speed and authentication accuracy

1.5 LIMITATION OF STUDY
The implementation of a nose and thumbprint-based system offers profound benefits for modern academic administration. Traditionally, manual logbooks were easily misplaced or falsified, leading to security breaches. This system eliminates the need for physical library cards, which are frequently lost or shared among students, thereby ensuring that only the registered individual can access resources.
Furthermore, the study contributes to the field of Computer Science by exploring multimodal fusion. While single-fingerprint systems can fail due to worn ridges or skin injuries, the addition of a non-contact trait like the nose ensures continuous accessibility. For library staff, this automation reduces the clerical workload, allowing for real-time tracking of overdue books and inventory patterns, ultimately improving the library’s operational throughput.

1.6 OPERATIONAL DEFINITION OF TERMS
Fingerprint: This refers to the unique impression or anatomical mark produced by the friction ridges of a human fingertip. It is a critical biometric identifier due to the distinct and non-replicable patterns of whorls and lines found on each individual's skin.
Nose Recognition (Nasal Biometrics): A physiological biometric trait that identifies individuals based on the unique geometry and spatial coordinates of the nose, including the bridge and nostrils.
Biometrics: A broad category of science involving the measurement and analysis of unique physiological or behavioral characteristics used for identity verification. These include thumbprints, facial landmarks, iris patterns, and vocal signatures.
Biometric Verification: The systematic process of evaluating one or more distinct biological traits to uniquely identify and authenticate a person's identity.
Scanner: A specialized electronic device designed to examine, read, or monitor physical attributes to convert them into digital data for processing.
Fingerprint Sensor: A hardware component utilized to capture a high-fidelity digital image of a thumbprint's ridge patterns for template generation.
Information System: A structured framework comprising procedures, human actors, instructions, and hardware equipment designed to process data into meaningful information.
Technology: The practical application of specialized techniques and resources to organize information and accomplish specific objectives that benefit society.
Information: The processed output of gathered, transmitted, and retrieved data items that are synthesized to convey a specific, actionable message.
Computer Network: A communication infrastructure that facilitates the interconnection of two or more computing devices via physical or wireless links.
Database: A structured repository of electronic data organized to allow for automated manipulation, retrieval, and management. This is also frequently referred to as a databank.
Database Management System (DBMS): The software interface and engine responsible for the systematic management, storage, and querying of database records.
File Transfer: The protocol or mechanism by which digital assets, such as spreadsheets, graphics, or media files, are transmitted between users over a network.
Database Table: A logical storage unit within a database consisting of rows and columns used to organize data for efficient retrieval.
Transaction: A logical unit of database work that involves a group of operations which must be executed successfully as a single, atomic action.
Encapsulation: An object-oriented programming concept that involves bundling data and methods while restricting direct access to the internal state of an object.
Class: A blueprint or prototype in software engineering from which individual objects are instantiated.
Use Case Diagram: A visual representation used in system analysis to illustrate the various interactions between users (actors) and the system to define functional requirements.
Flowchart (Activity Diagram): A graphical model within the Unified Modeling Language (UML) that represents the step-by-step logic, workflows, and decision paths of a system process.








CHAPTER 2
2.1 OVERVIEW OF MULTIMODAL BIOMETRIC LIBRARY SYSTEM
A library management system integrated with multimodal biometrics represents a significant advancement over single-modality frameworks. By combining two distinct biological traits the nose and the thumb the system automates user enrollment, book tracking, and access control with higher reliability. Extensive external research demonstrates that fusing multiple biological markers mathematically mitigates the false rejection rates that frequently plague standalone biometric sensors (Ross, Nandakumar, & Jain, 2006). The workflow generally consists of
User Enrollment: The concurrent scanning of the user’s thumbprint and nasal landmarks to generate a fused biometric template.
Resource Management: Assigning unique identifiers to library books and updating their status in a centralized database.
Identity Verification: Cross-referencing live biometric inputs against stored templates to authenticate students.
Transaction Logging: Automating the borrowing and return processes, thereby adjusting the book's availability status in real-time.

2.2 WHAT IS BIOMETRICS
At its core, biometrics represents the scientific discipline dedicated to evaluating and quantifying distinct biological or behavioral characteristics.
Within the realm of information technology, this translates to utilizing specialized systems that analyze physical traits such as thumb impressions, facial contours, iris geometry, and voice signatures to establish absolute proof of identity.
The foundational logic driving this technology is that every human possesses intrinsic physical attributes that are impossible to duplicate, making them perfect candidates for algorithmic verification(Jain, Ross, & Prabhakar, 2004).
Unlike conventional security mechanisms, such as numeric passcodes or physical keys which can easily be compromised, stolen, or forgotten, biological markers offer a far superior tier of protection.
Furthermore, because the raw biometric data is typically encrypted and stored as mathematical templates rather than literal images, the risk of identity theft is heavily mitigated (Wayman, 2005).

2.3 HISTORY OF BIOMETRICS
The term "biometrics" finds its linguistic origins in the Greek lexicon, combining "bio," which translates to life, and "metrics," meaning to measure. Even though we usually think of computers and scanners when we hear the word today, the basic idea is actually thousands of years old, with the ancient Chinese and Egyptians playing a huge role in the early history of identifying people by their physical traits. Of course, automated systems only really took off in the last few decades thanks to major leaps in computer processing and digital imaging (Prabhakar, Pankanti, & Jain, 2003) . Today, the main focus has shifted toward things like iris scans, facial recognition, and fingerprints to boost security and stop terrorism.
Looking at the first real documented cases in 1858. Sir William Herschel, who worked for the Civil Service of India, started making his employees put their handprints on the back of their work contracts. It was a simple but highly effective way to tell the workers apart. Then, a bit later in 1870, a man named Alphonse Bertillon came up with a whole new system. He didn't use fingerprints. Instead, his method called "Bertillonage" or anthropometrics relied completely on taking detailed photographs and recording very specific body measurements of people. It worked for a while. However, police eventually dropped the system around 1903 once they realized a major flaw: different people can actually have the exact same physical measurements.(Komarinski, 2004)
Just before Bertillon's system was scrapped, Sir Francis Galton made a massive breakthrough in 1892. He created a way to classify fingerprints by looking at specific little details called minutiae characteristics. Surprisingly, researchers and educators still use his basic classification system today. As the field grew, it needed formal education. By 1920, the FBI teamed up with West Virginia University to offer the very first Bachelor’s Degree program in biometrics. They even consulted with the International Association for Identification to put the curriculum together.
Fast forward to the 2000s, and the technology really started to become standardized on a global scale. In 2003, the US government set up a special Subcommittee on Biometrics to handle research, policy, and international teamwork. That same year, on May 28, the International Civil Aviation Organization (ICAO) agreed on a worldwide plan to start putting biometric data into machine-readable travel documents. Over in Europe, the European Commission threw its support behind a new independent group called the European Biometrics Forum, hoping to make the EU a world leader in the industry by breaking down market barriers.
2004 was a massive year for putting these systems into actual practice. The US-VISIT program officially launched, which meant visitors needing a visa suddenly had to provide digital photographs and inkless fingerprint (Gelb & Clark, 2013). This allowed border agents to easily check if someone was a known security risk or if they had overstayed a previous visa. The Department of Defense also rolled out their Automated Biometric Identification System (ABIS) to track threats. It was incredibly thorough. It collected ten rolled fingerprints, five mugshots, voice samples, iris images, and even oral swabs for DNA from captured insurgents. Also in 2004, President Bush signed a directive making it mandatory for all federal employees to carry a smart ID card containing two stored fingerprint templates. On the state level, places like California, Rhode Island, and Connecticut started building massive palm print databases so police could share and search for known offenders.
Then, the market opened up even more in 2005. The broad US patent that originally covered the basic idea of iris recognition finally expired. This was a big deal because it gave other companies the chance to legally develop and market their own iris algorithms, even though the specific "IrisCodes" patent held by Dr. Daugman didn't expire until 2011. Technology was moving fast. At a 2005 conference, the Sarnoff Corporation showed off a system called "Iris on the Move," which could actually capture a person's iris data while they were just walking normally through a doorway. And through all of this rapid development, fingerprint recognition remained one of the most reliable and popular methods out there, simply because matching ridges and minutia points is so accurate.(Bowyer, 2004).)
2.4 BIOMETRIC RECOGNITION SYSTEMS
A biometric recognition system is an automated system designed to identify or verify individuals based on their unique physiological or behavioral characteristics. Unlike traditional authentication methods such as passwords, identification cards, or PINs, biometric systems rely on intrinsic human traits that are difficult to duplicate or transfer. This makes them highly reliable for secure access control and identity management in modern information systems (Jain, Ross, & Prabhakar, 2004).
Biometric recognition operates in two primary modes: identification and verification. Identification is a one-to-many matching process in which an input biometric sample is compared against multiple stored templates in a database to determine the identity of an individual. Verification, on the other hand, is a one-to-one comparison that confirms whether a user is who they claim to be (Wayman, 2005).
The increasing need for enhanced security and automation has led to the widespread adoption of biometric systems across various domains, including banking, healthcare, and education (Prabhakar, Pankanti, & Jain, 2003).
2.5 ARCHITECTURE OF BIOMETRIC RECOGNITION SYSTEM
A typical biometric recognition system consists of several functional modules that work together to perform identity recognition. These components form a structured pipeline that ensures accurate and efficient processing of biometric data (Bolle et al., 2004).
The first component is the data acquisition module, which captures raw biometric data from the user through sensors such as fingerprint scanners or cameras. The quality of data obtained at this stage directly affects system performance.
Following this is the pre-processing module, where the captured data is enhanced using techniques such as normalization, noise reduction, and grayscale conversion to ensure consistency (Bradski & Kaehler, 2008).
The feature extraction module identifies and extracts unique characteristics from the biometric data. These features are converted into a compact numerical representation known as a biometric template, reducing computational complexity while preserving essential information.
The template storage module securely stores these templates in a database, typically in encrypted form to protect user privacy.
The matching or classification module compares new biometric inputs with stored templates using pattern recognition algorithms such as k-Nearest Neighbors, Support Vector Machines, or neural networks (Duda, Hart, & Stork, 2001).
Finally, the decision module determines whether access should be granted or denied based on the matching results.
2.6 TYPES OF BIOMETRIC RECOGNITION SYSTEMS
Biometric recognition systems are broadly classified into unimodal and multimodal systems.
Unimodal systems rely on a single biometric trait, such as fingerprint or facial recognition. While these systems are simple and cost-effective, they are often susceptible to noise, spoofing attacks, and environmental factors (Maltoni et al., 2009).
Multimodal systems combine two or more biometric traits to improve accuracy and reliability. By integrating multiple sources of biometric data, these systems significantly reduce error rates and enhance resistance to spoofing attempts (Ross, Nandakumar, & Jain, 2006).
The system developed in this study is a multimodal biometric recognition system that integrates thumbprint recognition with facial landmark analysis, thereby improving robustness and system performance.

2.7 WORKING PRINCIPLE OF A BIOMETRIC RECOGNITION SYSTEM
The operation of a biometric recognition system follows a sequential pipeline consisting of data acquisition, preprocessing, feature extraction, matching, and decision making (Jain et al., 2004).
The process begins with data acquisition, where biometric input is captured using sensors. This is followed by pre-processing, where the captured data is cleaned and enhanced to remove noise and improve quality.
Next, the system performs feature extraction, converting the biometric data into a compact and distinctive representation. The extracted features are then compared with stored templates during the matching phase, where similarity measures are computed.
Finally, the decision phase determines whether the input matches a stored template based on a predefined threshold, thereby granting or denying access.

2.8 RELEVANCE OF BIOMETRIC RECOGNITION SYSTEMS TO THIS STUDY
The application of biometric recognition systems in library management addresses the limitations of traditional identification methods such as manual records and library cards. These conventional systems are prone to loss, duplication, and unauthorized access, which can compromise security and operational efficiency (Oloyede & Alaya, 2013).
By incorporating biometric recognition, the system developed in this study ensures accurate user identification and enhances system security. The integration of thumbprint recognition provides a reliable physiological biometric, while facial landmark recognition introduces a non-contact modality that improves usability and accessibility.
Furthermore, the use of a multimodal approach reduces the likelihood of system failure and enhances robustness. If one biometric modality is affected by environmental conditions, the other can still facilitate accurate identification.
Advanced techniques such as Independent Component Analysis for feature extraction and k-Nearest Neighbors for classification further improve system efficiency and accuracy, making the proposed system suitable for modern library environments.


2.9 OTHER APPLICATIONS OF BIOMETRICS
 While the deployment of biometric authentication is highly beneficial for academic library management, its utility extends far beyond educational institutions. The technology is currently being leveraged across a diverse array of sectors, including government administration, commercial enterprises, forensic science, and border security, to establish irrefutable proof of identity.
Public Sector and Government Operations: Government agencies heavily rely on biometric data for the issuance of national identity cards, driver's licenses, passports, and managing border control. By storing this biometric data on secure chips within residence permits or passports, authorities can reliably cross-reference an individual's live scanned fingerprint against the central databank (Gelb & Clark, 2013).
Commercial and Corporate Integrations: In the corporate sector, biometrics are routinely deployed to secure access to internal computer networks, protect electronic commerce transactions, and authenticate ATM and credit card usage. Reliable customer identification has revolutionized digital trading and physical access control. Furthermore, biometric sensors such as USB thumbprint scanners, iris readers, or facial recognition cameras are increasingly replacing traditional employee punch cards. This allows corporations to effortlessly monitor employee attendance and precise working hours, ensuring that staff members clock in and out accurately without the vulnerabilities of legacy systems. (Prabhakar et al., 2003)
Educational and Corporate Institutions: Time management and attendance tracking in various institutions are frequently secured through biometrics. Traditional access control methods, such as PIN codes or swipe badges, are easily compromised; employees or students can forget their codes, lose their physical badges, or engage in "buddy punching," where a colleague fraudulently clocks in on their behalf. By transitioning to biometric validation, institutions eliminate these deceptive practices. In academic settings, this technology is exceptionally valuable for validating student identities during critical events such as examinations, laboratory sessions, or mandatory tutorials. Automating this identity verification process curbs the presence of imposters and drastically reduces the overhead costs associated with deploying manual security personnel. (Oloyede & Alaya, 2013)
Forensic Science and Law Enforcement: The law enforcement community utilizes biometric identification for criminal investigations, terrorist tracking, missing children location, and corpse identification. Police departments have relied on friction ridge analysis for over a century, gaining a massive operational advantage by maintaining extensive databases of known offenders' fingerprints, DNA profiles, and facial photographs. Automated Fingerprint Identification Systems (AFIS) empower forensic investigators to rapidly compare latent prints extracted from crime scenes against millions of stored criminal records, facilitating swift and accurate suspect identification. Additionally, biometric screening is increasingly utilized in public venues and investigative scenarios to match physical evidence and secure environments. (Maltoni et al., 2009)
2.10 ANATOMICAL PATTERNS OF FINGERPRINTS
Arches: In this structural formation, the dermal ridges enter the fingertip from one margin, elevate near the center to form a mound or tent-like arc, and subsequently flow out the opposite margin.
Loops: This pattern features ridges that enter from one distinct edge of the finger, curve abruptly backward, and exit toward the exact same edge from which they originated.
Whorls: In a whorl pattern, the friction ridges spiral or form concentric circular shapes directly around the central core of the fingertip.


Figure 2.1: Finger patterns ( Source: Gonzalez and Woods, 2002

Figure 2.2: Fingerprint minutia features (Source: Gonzalez and Woods, 2002)


2.11 MICROSCOPIC MINUTIAE CHARACTERISTIC
While the macro-patterns provide a general classification framework, the true uniqueness of a fingerprint lies in its micro-details, scientifically referred to as minutiae. These are the specific, localized points where ridge lines exhibit sudden changes. The primary minutiae characteristics include the ridge ending, which is the precise location where a friction ridge abruptly terminates. Another critical feature is the bifurcation, defined as the specific point where a single, continuous ridge splits into two distinct paths. Additionally, the anatomy features short ridges (or dots), (Maltoni et al., 2009) which are isolated ridge segments that are significantly shorter than the average ridge lines found on the print. Because there is no historical or scientific record of any two individuals possessing the exact same minutiae configuration, extracting and mathematically mapping these specific markers provides an exceptionally reliable and secure foundation for automated identity verification.

2.12 FINGERPRINT SCANNER
A fingerprint scanner is essentially an electronic device specifically engineered to grab a digital picture of the unique patterns on a person's fingertip. In biometric terminology, this initial raw picture is usually called a "live scan". Once the scanner successfully captures the image, the internal system processes it digitally to extract specific minutiae features, ultimately creating what we know as a biometric template. This secure template is then locked away in a centralized database so it can be utilized for future matching.
You will find basic scanners that only capture a flat, two-dimensional image of the print. However, if you invest in more advanced hardware, the scanners can actually capture the three-dimensional shape and size of the thumb. Some high-end scanners even feature "liveness" detection by checking for the presence of blood pulsing beneath the skin. This makes it incredibly difficult for someone to duplicate a print or spoof the system with a fake silicone finger (Marcel, Nixon, & Li, 2014)
The actual image acquisition inside the device usually happens through one of two main methods: optical scanning or capacitance sensing. Because the physical ridges and furrows on our fingers naturally form a pattern that cannot be altered or removed unless there is a severe physical injury this hardware provides a highly reliable way to enroll and verify users. A complete, standard security setup basically consists of the scanning sensor itself, a computer processor to handle the data, and specialized software that automatically compares new scans against the stored database records to either allow or disallow access.

2.13 FINGERPRINT AUTHENTICATION SYSTEMS
A fingerprint authentication system is a complete biometric security framework that relies entirely on a person's unique fingertip patterns to verify their identity. The core process is actually quite straightforward. It starts by mapping the specific valleys and ridges of the user's fingertip to build a secure digital representation, or template.
When a student or staff member wants to access the library's resources, they simply place their finger on the sensor. The system's software then instantly compares this new, live scan with the template already securely saved in the database. If the two match up perfectly, the user is verified and granted access. This seamless and fast process is exactly why you see fingerprint authentication built into almost everything today, from modern smartphones to laptops, offering a perfect blend of high security and user convenience. To make this authentication happen, the system runs through a few highly specific technical stages.

2.13.1 IMAGE ACQUISITION.
The very first step in the pipeline is image acquisition. In the fields of machine vision and digital image processing, this simply refers to the action of retrieving an image directly from a hardware source. For a multimodal library system, this hardware involves utilizing the optical fingerprint sensor alongside the digital camera. Without successfully pulling this initial raw image from the sensors, the rest of the verification process simply cannot happen.


2.13.2 CONVERSION OF FINGERPRINT INTO GREYSCALE.
Greyscale images are fundamentally created from continuous tone photographs, stripping away complex color data to leave just black, white, and varying shades of gray. Historically, physical photographs were digitized using desktop scanning equipment and saved as computer files. In modern biometric software, shifting the live scan to greyscale drastically reduces the computational load while highly boosting the visual contrast, making it much easier for the algorithm to "see" the fingerprint ridges (Bradski & Kaehler, 2008)

2.13.3 NORMALIZATION OF FINGERPRINT
Normalization is a critical pre-processing step designed specifically to boost the overall quality of the scanned image before any matching occurs. It achieves this by aggressively stripping out background noise and altering the entire range of pixel intensity values.
The algorithm looks closely at the mathematical mean and variance of the image's pixels. By systematically adjusting these factors, the normalization process successfully reduces the extreme variations in gray-level values found along the ridges and valleys of the thumbprint. Ultimately, this step creates a clean, uniform image, ensuring that the feature extraction algorithm can read the minutiae without making costly errors.
2.14 NOSE AND FACIAL LANDMARK BIOMETRICS
When we think about facial recognition, the mind usually jumps to scanning the entire face. However, zeroing in on specific facial landmarks particularly the nose is rapidly emerging as a highly reliable biometric strategy. What exactly is nose recognition, or nasal biometrics? Simply put, it is a physiological biometric trait that identifies individuals by analyzing the unique geometry and spatial coordinates of their nose. This involves looking closely at distinct features like the bridge and the nostrils. By isolating these specific landmarks, the system can create a highly accurate mathematical map of the user's face.
But why use the nose, especially in a library setting? The answer lies in the vulnerabilities of using just one biometric trait. Single-modality systems, like traditional fingerprint scanners, are incredibly useful but they definitely have weak points. For example, a student might have a temporary thumb injury, like a cut or a burn. They might just have dust or sweat on their hands (Ross et al., 2006). In a traditional system, these minor issues would cause the sensor to reject a legitimate student, creating frustrating bottlenecks at the library desk. Furthermore, basic fingerprint scanners often struggle to tell the difference between a real, live finger and an artificial fake.
By bringing nose-tip landmarks into the equation alongside the thumbprint, the system suddenly gains a much higher tier of security. It introduces a critical element of "liveness" detection. Because the nose is a non-contact trait, it ensures continuous accessibility even if the student's hands are injured or dirty. If the fingerprint scanner fails, the system still has a complex facial landmark to rely on, effectively minimizing the risks of a single-point biometric failure.
To actually capture this data, the system does not need wildly expensive hardware. A standard, high-resolution digital camera is used to capture the facial nose landmarks while an optical scanner concurrently reads the thumbprint. Once the camera takes the image, the software looks for specific geometric anchor points. The extraction algorithm typically focuses on three or four main regions. First, it maps the nasion, or the root of the nose directly between the eyes. Then, it measures the exact length and width of the nasal bridge down to the pronasale, which is the prominent tip of the nose. Finally, the system calculates the distinct spatial geometry of the alae, or the nostrils.(Lugaresi et al., 2019)
Because the underlying bone structure and cartilage of the nose rarely change after a person reaches adulthood, these spatial coordinates remain incredibly stable over time. creating a virtually tamper-proof profile when fused with the thumbprint (Zafeiriou et al., 2015)Even if a student changes their hairstyle, puts on glasses, or changes their facial expression, the rigid geometry of the nose remains largely unaffected. Once these unique coordinates are captured by the camera, the system translates them into a secure digital template. This nose template is then fused with the thumbprint data to create a tamper-proof, dual-layer authentication profile that is virtually impossible for an imposter to replicate

2.15 FEATURE EXTRACTION
Once the system has successfully captured and cleaned up the normalized images of the user's thumbprint and nasal landmarks, it still cannot just feed those raw pictures directly into a matching algorithm. Raw pixel data is simply too bulky and complex for a system to process quickly. Instead, the software has to pull out the most important, identifying markers a critical process known as feature extraction.
Basically, this step transforms the raw image data into a highly compressed, numerical format while making sure to keep all the original, unique biological information perfectly intact. By boiling the image down to just its core mathematical features, the system achieves much faster and far more accurate results than it ever would if it tried to apply machine learning directly to an unedited photograph. While researchers use a wide variety of techniques to accomplish this such as Gabor filters, Principal Component Analysis (PCA), or Local Binary Patterns this specific multimodal project relies on a highly robust method known as Independent Component Analysis (ICA).

2.16 INDEPENDENT COMPONENT ANALYSIS (ICA)
In a multimodal setup, the system is dealing with a massive amount of complex, overlapping data coming from both the friction ridges of the thumb and the spatial geometry of the nose. ICA is a powerful statistical technique designed specifically to take mixed, multivariate signals and separate them into completely independent, non-overlapping components.(Hyvärinen & Oja, 2000) Essentially, it cuts through the background "noise" to isolate the unique, hidden biometric signatures inside high-dimensional data.
Below is the mathematical pipeline the system uses to actually achieve this extraction:
1. Data Preprocessing and Centering:
Before the algorithm can successfully find the independent features of a student's nose or thumb, it has to put all the data on an even playing field. It does this by centering the dataset. The system calculates the mean of the biometric features and then subtracts that mean, ensuring that all the features revolve perfectly around zero. This crucial first step is represented by the following equation:
Xc = X − μ
Where X is the original matrix of the combined nose and thumbprint features, and μ represents the mean vector of that dataset.
2. Whitening (Sphering): The system needs to completely remove any redundancies or correlations between the different biometric traits. This step is known as whitening. It transforms the centered data so that its covariance matrix basically becomes an identity matrix. What this means in plain terms is that all the features are scaled equally in every direction, so no single trait dominates the others. The whitening equation looks like this:
Xw = D^(-1/2) E^T Xc
Here, Xw is our newly whitened data, E represents the matrix of eigenvectors, and D stands for the diagonal matrix of the eigenvalues.
3. Extracting the Independent Components: 
 Finally, the system runs an optimization algorithm (like FastICA) on the whitened data. It is actively looking for an "unmixing" matrix that maximizes the statistical independence of the final features. Once it successfully finds this matrix, it applies it to extract the final, unique biometric templates for both the nasal landmarks and the thumbprint. The final calculation is:
S = W Xw
Where S represents the final matrix of our distinct, independent components (the actual unique features), and W is the unmixing matrix that the algorithm learned during the process. By extracting these truly independent features, the system drops all redundant data, making the final classification step highly robust and incredibly hard to spoof.

This process summarizes how ICA decomposes fingerprint data into independent components that capture unique, non-overlapping features. By using these independent features, the system can reduce redundant data and focus on distinctive characteristics of each fingerprint, making it more robust for identification.
2.17 THE CLASSIFICATION PHASE
After the system has successfully extracted the independent, mathematical features from the student's nose and thumbprint using ICA.  This is where the classification phase steps in. In machine learning, classification is essentially the process of categorizing or assigning specific labels to new input data based on what the system already knows.
For a biometric system, this means taking the live data extracted from the scanner and camera, and matching it against the saved templates in the library's database to figure out exactly who is trying to log in. Researchers use a wide variety of algorithms to accomplish this. For example, some systems use Back Propagation Neural Networks, which adjust the weights of their connections based on error rates to "learn" patterns over time. Others might use Support Vector Machines (SVM) to draw complex boundary lines between data points, or rely on ensemble methods like Random Forest and Gradient Boosting. While all of these have their distinct strengths, this specific multimodal project utilizes a highly intuitive and robust algorithm known as k-Nearest Neighbors.


2.18 K-NEAREST NEIGHBORS (K-NN)
K-Nearest Neighbors, or k-NN for short, is a remarkably straightforward classification algorithm that relies on the basic concept of proximity or "closeness". When a student scans their thumb and face, the algorithm doesn't run the data through a massively complex, pre-trained neural network. Because k-NN is a non-parametric, instance-based learning method, it actually doesn't require a strict training phase at all. (Cover & Hart, 1967) Instead, it stores the entire dataset of registered students and uses that raw data directly to make its predictions.
When a new biometric scan is introduced into the system, k-NN plots that new data point in a virtual feature space. It then looks around to find the "k" number of saved training samples that are physically closest to it. It figures out this closeness by calculating a specific distance metric, most commonly the Euclidean distance. Once the algorithm identifies these nearest neighbors, it simply takes a vote. The class label or in this case, the student's identity is determined by a majority vote among those closest neighbors. Whichever identity holds the most votes is assigned to the new scan.
In a complex scenario where the system has to choose between hundreds of different students (a multi-class classification problem), k-NN handles the workload beautifully without needing separate binary classifiers. Mathematically, the decision function the system uses to assign the final identity looks like this:
f(x) = argmax c∈C ∑(xi,yi)∈Nk(x) ║(yi=c)  (Duda, Hart, & Stork, 2001)
In this equation, C represents the set of all possible student classes, Nk(x) stands for the set of the k nearest neighbors to our new biometric scan, and the indicator function ║ simply returns a 1 if there is a match and a 0 if there isn't.
Naturally, k-NN is not without its challenges. Because it physically calculates the distance for every single new scan against all the training samples, it can become computationally heavy and slow down if the dataset grows incredibly large
. It is also notoriously sensitive to irrelevant features in high-dimensional spaces
However, because this specific multimodal system already utilized ICA to perfectly clean, whiten, and compress the data into independent features, those primary vulnerabilities are successfully bypassed, allowing k-NN to operate with exceptional speed and accuracy
2.19 PERFORMANCE METRICS
As biometric technologies develop, it is absolutely critical to measure their real-world reliability and accuracy. To evaluate how well the k-NN algorithm is matching the nose and thumbprint data, the system's performance is graded using a few highly specific metrics, often calculated using a confusion matrix.

The primary parameters we analyze include:
False Positive Rate (FPR) / False Accept Rate (FAR): This is a critical security metric. It measures the percentage of times the system incorrectly grants access to an unauthorized person, essentially mistaking an imposter for a registered student
False Negative Rate (FNR) / False Reject Rate (FRR): This measures the system's convenience factor. It calculates how often the system incorrectly rejects a perfectly legitimate, registered student
Sensitivity (True Positive Rate): This metric defines the system's overall ability to successfully identify the presence of a legitimate fingerprint and facial image that actually exists in the created database
Specificity (True Negative Rate): Conversely, this measures the system's ability to successfully identify when a biometric scan does not belong to anyone in the database, ensuring imposters are blocked
Overall Accuracy: This is the ultimate bottom line. It calculates the total percentage of correct predictions both the correct acceptances of valid students and the correct rejections of imposters out of all the scans processed
Average Computational Time: Security shouldn't come at the cost of massive delays. This metric measures exactly how many seconds it takes for the backend software to process the live images, run the ICA extraction, execute the k-NN voting process, and return a final verdict (Bolle et al., 2004).
CHAPTER 3
3.1 METHODOLOGY
In this specific project, the traditional reliance on a single physical trait is entirely replaced by a dual-acquisition hardware setup capable of capturing high-resolution thumbprint images through an optical scanner and facial nose landmarks via a digital camera. To effectively build this multimodal biometric framework, the raw biometric data is securely grabbed by these hardware components and passed directly into the system's software architecture for classification.
The technical implementation of this multimodal project utilizes a Python backend, specifically leveraging the Django framework as the core Database Management System (DBMS) and server environment. Python is widely recognized in academic research for its robust integration with advanced machine learning and image processing capabilities (Van Rossum & Drake, 2009) Django was deliberately chosen because it provides a highly secure, scalable backend to manage student registrations, book issuance, and borrowing history (Holovaty & Kaplan-Moss, 2009), while ensuring strict user privacy by storing encrypted biometric hashes rather than raw image files.
To process the incoming physiological data, the system utilizes specialized computer vision libraries. OpenCV is deployed to handle the complex image pre-processing, normalization, and noise reduction of the thumbprint data. Concurrently, Google's MediaPipe framework is utilized to precisely map the spatial geometry and specific coordinates of the facial nose landmarks. Once these distinct features are extracted and refined using Independent Component Analysis (ICA), the system relies on the k-Nearest Neighbors (k-NN) algorithm to rapidly classify and match the users against the Django database.

3.2 STAGES OF THE MULTIMODAL SYSTEM DEVELOPMENT
Building a sophisticated, hybrid authentication system requires a strictly phased approach to ensure that data integrity is maintained from the moment the user steps up to the scanner. Establishing a clear pipeline is critical in multimodal systems to prevent data overlap and processing bottlenecks (Ross, Nandakumar, & Jain, 2006). The required sequential stages involved in developing this specific biometric recognition system are highlighted as follows:
STAGE 1: Multimodal Image Acquisition (Capturing both the nose landmarks and the thumbprint).
STAGE 2: Biometric Image Pre-processing utilizing OpenCV.
STAGE 3: Facial Landmark Extraction utilizing MediaPipe.
STAGE 4: Thumbprint Feature Extraction utilizing Independent Component Analysis (ICA).
STAGE 5: Training and Classification utilizing the k-Nearest Neighbors (k-NN) algorithm.
STAGE 6: Result Evaluation and Performance Benchmarking.

3.3 BIOMETRIC IMAGE ACQUISITION
The very first step in the pipeline involves gathering the raw biological data. The scope of this research and data collection is strictly focused on the LAUTECH community. To build a robust and comprehensive training dataset, the study utilizes a targeted sample size of 50 selected subjects. During the initial enrollment phase, the system captures multiple high-resolution samples from each participant to populate the Django database.
This is not a simple, single-scan process. The system actively utilizes the optical fingerprint sensor to record the friction ridges of the thumb, while the digital camera simultaneously maps the distinct spatial coordinates of the nose, capturing features like the nasal bridge and nostrils. All images are taken under relatively uniform illumination conditions with a light-colored background to prevent initial sensor confusion. Fusing these specific facial and friction-ridge traits significantly boosts the system's defense against presentation attacks and spoofing (Marcel, Nixon, & Li, 2014). By gathering multiple concurrent samples of both modalities from the 50 subjects, the Python database is populated with enough diverse data to thoroughly train the matching algorithm and accurately test the system's real-world reliability.

3.4.1    Contrast Adjustment
Adaptive histogram equalization is applied on acquired image. Adaptive histogram equalization maximizes the contrast throughout an image by adaptively enhancing the contrast of each pixel relative to its local neighborhood. This process will produce improved contrast for all levels of contrast (small and large) in the original image. For adaptive histogram equalization to enhance local contrast, histograms will be calculated for small regional areas of pixels, producing local histograms. These local histograms will then be equalized or remapped from the often-narrow range of intensity values indicative of a central pixel and its closest neighbor's to the full range of intensity values available in the display. Further, to enhance the edges, a sigmoid function (Siavash, 2017 and Roberto, 2013) in Equation (3.1) will be used:
y(x) =  M/1+e-(x-m-x/α)+ change in x                                                                    	(3.1)
where x is the original image, M is the image pixels representing large level of contrast of x, m is the image pixels representing small level of contrast x, delta x is the change in the original image in the contrast image and a is the change factor.
3.4.2    Image Conversion from RGB to HSV and YCBCR
The acquired images that have undergone contrast adjustment will be converted from the original colour models i.e. RGB to the HSV and YCRCR colour models. This is necessary to extract the sandy region indicating the unpaved trail. The pre-processing state prepares the acquired image for segmentation.

3.5 BIOMETRIC IMAGE PRE-PROCESSING UTILIZING OPEN CV
Raw images straight from a digital camera or an optical scanner are rarely perfect. They often contain environmental interference, varying lighting conditions, and sensor artifacts. Therefore, before the Django backend can attempt to identify a student, it must run the raw files through a strict pre-processing pipeline involving image normalization, noise reduction, and grayscale conversion. This pipeline is entirely powered by OpenCV, an industry-standard library widely cited for ensuring that biometric data maintains its mathematical integrity during manipulation (Bradski & Kaehler, 2008).
3.5.11 CONTRAST ADJUSTMENT AND NOISE REDUCTION
For the thumbprint images, the initial OpenCV pre-processing stage involves applying adaptive histogram equalization. Adaptive histogram equalization maximizes the contrast throughout an image by adaptively enhancing the contrast of each pixel relative to its local neighborhood. Instead of applying a single blanket adjustment to the entire photograph, histograms are calculated for small regional areas of pixels, producing local histograms. Localized contrast enhancement is a highly proven technique in computer vision for improving the clarity of complex friction ridges (Zuiderveld, 1994). These local histograms are then equalized, remapping the narrow range of intensity values to the full spectrum available. This successfully removes background noise and other unwanted elements from the biometric images, resulting in a significantly cleaner, thinned image.
To further enhance the edges of the friction ridges, a sigmoid function is utilized during this adjustment phase. The mathematical equation governing this contrast shift is represented as:
 y(x) = M / (1 + e^(-(x-m-x/α))) + Δx 
Where x represents the original image, M represents the image pixels showing a large level of contrast, m represents pixels with a small level of contrast, Δx is the change applied to the original image, and α serves as the core change factor.

3.5.2 IMAGE CONVERSION TO GRAYSCALE
Once the contrast is dynamically adjusted by OpenCV, the acquired images are converted from their original color models (RGB) into a Grayscale or HSV format. Because the physical color of a student's skin or the background lighting provides no actual mathematical value to the minutiae or spatial coordinates, keeping color data would only bog down the system. Stripping the complex color channels away drastically reduces the computational load on the server, preparing the acquired images perfectly for the feature extraction phase.

3.6 FEATURE EXTRACTION USING MEDIAPIPE AND ICA
After the images are cleaned, normalized, and converted to grayscale, they are passed into the extraction engines. Because this library management system deals with complex, overlapping data streams coming from two entirely different body parts, it utilizes a split-extraction method tailored to each specific trait.
3.6.1 NASAL LANDMARK EXTACTION VIA MEDIA PIPE
To capture the spatial geometry of the user's face, the Python backend deploys MediaPipe. MediaPipe's Face Mesh is exceptionally powerful at identifying rigid, non-contact facial anchor points in real-time. Google's MediaPipe architecture is heavily utilized in modern perception pipelines due to its highly optimized, cross-platform machine learning capabilities (Lugaresi et al., 2019). The extraction algorithm specifically focuses on mapping the nasion (the root of the nose directly between the eyes), measuring the exact length and width of the nasal bridge down to the pronasale (the prominent tip of the nose), and calculating the distinct spatial geometry of the alae (the nostrils). Because the underlying bone structure and cartilage of the nose rarely change after a person reaches adulthood, these spatial coordinates remain incredibly stable. MediaPipe pulls these specific geometric anchor points and translates them into a secure digital template.
3.6.2 THUMBPRINT FEATURE EXTRACTION VIA ICA
To extract the features from the thumbprint, the system relies on Independent Component Analysis (ICA). ICA is a statistical method specifically designed to take a mixed, multivariate signal and separate it into additive, completely independent components. ICA is widely recognized in academic research for its effectiveness in isolating non-Gaussian biological signatures from highly overlapping biometric datasets (Hyvärinen & Oja, 2000). The Django backend achieves this extraction through a highly structured mathematical process:
1. Standardizing and Centering the Data: ICA begins by standardizing and centering the dataset, ensuring each feature has a zero mean and unit variance. Centering is achieved mathematically by subtracting the mean vector of the dataset from the original matrix of biometric features. This is represented as: Xc = X − μ        Where X represents the original dataset matrix, and μ represents the mean vector.
2. Whitening the Data (Sphering): Following the centering process, the system applies a critical transformation known as whitening. Whitening forces the data to become entirely uncorrelated and standardized, transforming the data in such a way that the covariance matrix becomes an identity matrix. The whitening transformation equation is given by: X_whitened = V D^(-1/2) V^T Xc        (Equation 3.3) Where V and D represent the eigenvectors and eigenvalues extracted from the covariance matrix of Xc.
3. Extracting Independent Components: Finally, the ICA algorithm seeks to isolate the truly independent components by maximizing the non-Gaussianity within the whitened data. Using optimization algorithms, the system computes an unmixing matrix to isolate the underlying unique sources. The final independent feature vectors are extracted using the equation: S = W X        (Equation 3.4) Where S represents the final matrix of independent components, and W is the unmixing transformation matrix learned by the algorithm. These newly extracted thumbprint features are then fused with the MediaPipe nasal coordinates and passed to the classification phase.
3.7 CLASSIFICATION USING K-NEAREST NEIGHBORS (KNN)
Once the unique biological signatures of the nose and thumbprint have been cleanly extracted, the system must definitively match them to a registered student within the Django database. To accomplish this, the system deploys the k-Nearest Neighbors (k-NN) classification algorithm. K-NN is an instance-based learning method that memorizes the entire dataset of 50 LAUTECH subjects directly, allowing it to adapt instantly to new library registrations without requiring a lengthy retraining phase. By analyzing the closest training examples directly within the local feature space, k-NN serves as a highly reliable, non-parametric prediction model (Cover & Hart, 1967).
The system executes the k-NN classification through the following sequence:
1. Defining 'k': The very first parameter the system establishes is the value of k, which dictates the exact number of neighboring data points the algorithm will evaluate. To find the optimal balance for the library's database, the Python backend utilizes cross-validation, systematically testing different values until it identifies the one that yields the highest classification accuracy.
2. Calculating Distances: When a student scans their thumb and face, the newly extracted features are plotted into the system's feature space. K-NN then calculates the physical distance between this new data point and every existing template in the training set using the Euclidean distance metric. The mathematical formula applied by the software is: d(x,x') = √ (∑ (x_j − x_j')^2)      Where x and x' represent the two respective data points being measured in the feature space, and n represents the number of features.
3. Voting and Final Identity Assignment: After the Euclidean distances are calculated, the algorithm successfully isolates the k points in the training database that are physically closest to the live scan. Because identifying a single student is a multi-class problem, the classifier evaluates all possible identities simultaneously, assigning the final class label based on a simple majority vote among those nearest neighbors.
This multi-class decision function is mathematically represented as: f(x) = argmax_c∈C ∑_{(x_i, y_i)∈N_k(x)} ║(y_i = c)        (Equation 3.6) Where C represents the set of all possible student identities, N_k(x) is the set of the k nearest neighbors to the live biometric scan, and the indicator function ║ simply returns a 1 if there is a match to class c and a 0 if there is no match.

3.8PERFORMANCE MEASURES OF THE DEVELOPED SYSTEM
To definitively prove that combining nose-tip landmarks with thumbprint verification provides a higher tier of security than traditional models, the developed system's performance is rigorously evaluated. The system calculates its performance using a confusion matrix, measuring the True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN). Utilizing these matrix elements is a globally recognized academic standard for quantifying the reliability of binary and multi-class classification models (Fawcett, 2006).
Using these matrix values, the system is specifically benchmarked against the following core performance metrics to measure its reliability:
Sensitivity: Ability to successfully identify the presence of a legitimate multimodal fingerprint and facial image that actually exists in the created database. Sensitivity = TP / (TP + FN) x 100        
Specificity: Ability to successfully identify the absolute absence of a registered biometric image, ensuring unauthorized individuals are kept out. Specificity = TN / (TN + FP) x 100        
False Positive Rate (FPR): The proportion of imposters that the system incorrectly accepts. Minimizing this number is the primary goal of the dual-biometric approach. False Positive Rate = FP / (TN + FP) x 100       
Overall Accuracy: The ultimate baseline metric that calculates the total percentage of correct predictions made by the k-NN algorithm. Overall Accuracy = (TP + TN) / (TP + TN + FP + FN) x 100     
Average Recognition Time: Because the system must handle high-volume library traffic without causing bottlenecks, it calculates the average computational time required to process the dual-biometric capture, run the extractions, and execute the k-NN classification. Average recognition time = Total Recognition Time / Number of recognized scans   






REFERENCES
Adeoti-Adekeye, W. B. (1997). The importance of management information systems (MIS) in library administration.
Bolle, R. M., Connell, J. H., Pankanti, S., Ratha, N. K., & Senior, A. W. (2004). Guide to biometrics. Springer.
Bowyer, K. W. (2004). Face recognition technology: Security versus privacy. IEEE Technology and Society Magazine, 23(1), 9–19.
Bradski, G., & Kaehler, A. (2008). Learning OpenCV: Computer vision with the OpenCV library. O’Reilly Media.
Cover, T. M., & Hart, P. E. (1967). Nearest neighbor pattern classification. IEEE Transactions on Information Theory, 13(1), 21–27.
Duda, R. O., Hart, P. E., & Stork, D. G. (2001). Pattern classification (2nd ed.). Wiley.
Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861–874.
Gelb, A., & Clark, J. (2013). Identification for development: The biometrics revolution. Center for Global Development.
Gonzalez, R. C., & Woods, R. E. (2002). Digital image processing (2nd ed.). Prentice Hall.
Holovaty, A., & Kaplan-Moss, J. (2009). The definitive guide to Django: Web development done right. Apress.
Hyvärinen, A., & Oja, E. (2000). Independent component analysis: Algorithms and applications. Neural Networks, 13(4–5), 411–430.
Jain, A. K., Ross, A., & Prabhakar, S. (2004). An introduction to biometric recognition. IEEE Transactions on Circuits and Systems for Video Technology, 14(1), 4–20.
Komarinski, P. (2004). Automated fingerprint identification systems (AFIS). Elsevier Academic Press.
Lugaresi, C., Tang, J., Nash, H., McClanahan, C., Uboweja, E., Hays, M., Zhang, F., Chang, C. L., Yong, M. G., Lee, J., & others. (2019). MediaPipe: A framework for building perception pipelines. arXiv preprint arXiv:1906.08172.
Maltoni, D., Maio, D., Jain, A. K., & Prabhakar, S. (2009). Handbook of fingerprint recognition (2nd ed.). Springer.
Marcel, S., Nixon, M. S., & Li, S. Z. (2014). Handbook of biometric anti-spoofing: Presentation attack detection. Springer.
Oloyede, M. O., & Alaya, S. M. (2013). Fingerprint biometric authentication for library management system. International Journal of Computer Applications.
Prabhakar, S., Pankanti, S., & Jain, A. K. (2003). Biometric recognition: Security and privacy concerns. IEEE Security & Privacy, 1(2), 33–42.
Ross, A., Nandakumar, K., & Jain, A. K. (2006). Handbook of multimodal biometrics. Springer.
Van Rossum, G., & Drake, F. L. (2009). Python 3 reference manual. CreateSpace.
Wayman, J. L. (2005). Biometric systems: Technology, design and performance evaluation. Springer.
Zafeiriou, S., Zhang, C., & Zhang, Z. (2015). A survey on face detection in the wild: Past, present and future. Computer Vision and Image Understanding, 138, 1–24.
Zuiderveld, K. (1994). Contrast limited adaptive histogram equalization. In P. S. Heckbert (Ed.), Graphics gems IV (pp. 474–485). Academic Press.





