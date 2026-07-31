---
title: "On Regulated-Tech in Indonesia"
date: 2021-01-02T10:26:54
lastmod: 2021-01-02T10:27:27
slug: "security-considerations-for-regulated-tech-in-id"
draft: false
categories:
  - "Regulation"
---

Note that this document created in mid-2020 where on 24 January 2020, President Joko Widodo signed the Personal Data Protection (PDP) Bill which is currently being finalized by the Indonesian House of Representatives (DPR). Upon finalization of this PDP Bill, Indonesia will become the fifth country in ASEAN to implement regulations regarding Personal Data Protection. 

For the existing Personal Data Controller, there will be a two-year period before the PDP Bill is fully effective and achieves full compliance. 

The protection of personal data in Indonesia was initially focused on protection from a privacy perspective. Under the Indonesian Constitution,  the concept of privacy rights has been recognized and protected as part of the general concept of human rights. With the need to cover the sector yet to be regulated, specifically, that of the internet and electronic transaction-related activities, Law No. 11/2008 on Electronic Information and Transactions as amended by Law No. 19/2016 (collectively, the EIT Law) was passed. Even though most of the provisions of the EIT Law focus on electronic transactions, there is a notable provision that deals with personal data in the EIT Law. 

Similar to the individual concept in the Indonesian Constitution, article 26(1) of the EIT Law (along with its official elucidation) recognizes the protection of personal data as a part of privacy rights. The article further mentions that privacy rights shall include, among others, the right to monitor the access of information concerning private life and data. To further the effort to satisfy the need for effective protection of personal data, the Minister of Communications and Informatics (the MoCI) issued MoCI Regulation No. 20/2016 on Protection of Personal Data in Electronic Systems (MoCI Regulation 20). 

MoCI Regulation 20 is issued as mandated under Article 15(3) of Government Regulation No. 82/2012 on the Implementation of Electronic Systems and Transactions (GR 82), which requires personal data protection in electronic systems to be regulated by a Ministerial Regulation. MoCI Regulation 20 came into effect on 1 December 2018, and it applies only to PII stored in electronic systems, but not to PII that is stored manually.

MoCI Regulation 20 requires an Electronic System Operators (ESO) to notify the data subjects for the processing of personal data, through which the ESO also obtains the user’s consent. Other than the requirement that the consent needs to be in writing (either manually or electronically) and be prepared in Bahasa Indonesia, MoCI Regulation 20 does not expressly regulate the content of the consent. In practice, the notification usually covers the collected information, processing purposes and activities, the possibility to share or transfer collected information, access towards collected information, contact details of the ESO, and so on.

For healthcare data, the processing shall comply with Health Law No. 36 of 2009 and MOH Regulation 269. Under article 57 of the Health Law, every person is entitled to the confidentiality of his or her private health conditions that have been disclosed to healthcare providers. These private health conditions, which under MOH Regulation 269 are defined as medical records, shall be considered as personal data.

Under GR 82 and MoCI Regulation 20, an ESO has a general obligation to maintain confidentiality, implement adequate security and organizational measure, and develop an internal data protection policy. In addition, for the purpose of security measure for PII protection, MoCI Regulation 20 requires the following: 

  * an electronic system that is used for obtaining and collecting PII must have the capacity of interoperability and compatibility; 
  * electronic systems must use legal software;
  * electronic systems used in the process must be certified;
  * PII which is stored in an electronic system must be in the form of encrypted data;
  * storage of PII in an electronic system must be performed in accordance with the provisions regarding the procedures and facilities for securing the electronic system; 
  * an ESO shall use (establish or rent) a data center and disaster recovery center located within the territory of Indonesia (for an electronic system for public purposes) and fulfill the minimum standards in information technology systems, information technology risk management, information technology safeguards, resistance to system faults and failure, and transfer of information technology system management; 
  * an ESO is required to notify the data subject if the ESO’s security system has been breached; and
  * for overseas transfer of PII, in addition to the general conditions to obtain consent, MoCI Regulation 20 requires a party to (i) coordinate with the MOCI or authorized institutions; and (ii) implement relevant regulations regarding offshore transfer of PII.



In addition, according to MoCI Regulation 4, there is a mandatory certification for an electronic system having a high-level and strategic function (ie, related to sectoral or regional interest, public interest, national defense, and security).

#### PII & Sensitive Data Definition

Personally identifiable information (PII) is information that, when used alone or with other relevant data, can identify an individual. PII may contain direct identifiers (e.g., NIK, Passport Number) that can identify a person uniquely, or quasi-identifiers (e.g., Religion) that can be combined with other quasi-identifiers (e.g., date of birth) to successfully recognize an individual. Personally identifiable information (PII) can be sensitive or non-sensitive. Sensitive personal information includes legal statistics:

**PII Sensitive**  
---  
Full Name  
Nomor Induk Kependudukan  
Nomor Kartu Keluarga  
Nomor NPWP  
Nomor SIM  
Mother Maiden Name  
Passport Number  
Financial Information (e.g. Bank Account Number, Credit/Debit Card Number)  
Medical Record (e.g. Dental Image)  
Biometric Data  
Nomor Surat Tanda Registrasi (STR)  
Nomor Identifikasi PasienDental Clinic National Document (.e.g SIUP, TDP)  
_*including any images_  
  
The above list is by no means exhaustive and needs to be updated from time to time.**Regulated company needs to use anonymization techniques to encrypt, blurred, and obfuscate the PII,** so it is received in a non-personally identifiable form. This protection is not only limited to text but also media (e.g. image, video). Any usage of this data needs to follow the Principle of Least Privilege (POLP) and must be avoided to be exposed in any log management and prevent sensitive data vulnerabilities (e.g. IDOR).

Non-sensitive or indirect PII is easily accessible from public sources like phonebooks, the Internet, and corporate directories.

**PII Non-Sensitive**  
---  
Phone number  
Address  
Religion  
  
The above list contains quasi-identifiers and examples of non-sensitive information that may be released to the public (subject to follow Company policy). This type of information cannot be used alone to determine an individual’s identity. 

However, non-sensitive information, although not delicate, is linkable. This means that non-sensitive data, when used with other personal linkable information, can reveal the identity of an individual. De-anonymization and re-identification techniques tend to be successful when multiple sets of quasi-identifiers are pieced together and can be used to distinguish one person from another.

#### Data Location

Under MoCI Regulation 20, Electronic System Operators that provide public services were required by October 2017 to have data centers and disaster recovery centers in Indonesia as part of a business continuity plan. Based on the above provisions, the obligation to have a data center and a disaster recovery center in Indonesia only applies to Electronic Systems Operators that provide public services. However, there is no explicit definition of public services. 

It appears that "public services" means services provided by government institutions, state/government-owned entities, or other legal entities engaged for a state mission (as opposed to services of private entities that generally are provided to the public).

In any case, currently, there is no restriction on following a "mirroring" approach - that is, replicating data stored in offshore data centers and storing a copy in data centers located in Indonesia. We are aware that companies in Indonesia have implemented this approach to replicate the required data in local data centers without significant issues. As long as the data that is being stored in Indonesia is the same as what is stored in the offshore data center, this should not be an issue. 

The same treatment (i.e., no restriction on mirroring arrangements) is also implemented in other sectors, such as the financial sectors (e.g., banking, insurance, payment, and other financial services ). However, these sectors have specific requirements to store data outside of Indonesia (albeit not specifically on mirroring arrangements).

The MOCI regulation on electronic system registration only requires Electronic System Operators that provide public services to register their electronic systems with the MOCI. Notwithstanding the uncertainty in the definition of "public services", in practice, the MOCI has imposed the registration requirement on any local Electronic System Operators that generally provide their services to the public and/or make their services available to the public (such as social media companies, financial institutions, banking services, insurance companies, etc.).

Based on the above justifications, Regulated company need to follow these action steps:

  1. Register as Electronic System Operators (ESO) / Penyelenggara Sistem Elektronik (PSE) with MOCI on <https://pse.kominfo.go.id/>
  2. To have Data Mirroring/Replication in Indonesia Region
