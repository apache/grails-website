# Apache Grails Website

[![Documentation](https://img.shields.io/badge/Documentation-595959)](https://grails.apache.org/docs/)
[![Users Mailing List](https://img.shields.io/badge/Users_Mailing_List-feb571)](https://lists.apache.org/list.html?users@grails.apache.org)
[![Dev Mailing List](https://img.shields.io/badge/Dev_Mailing_List-feb571)](https://lists.apache.org/list.html?dev@grails.apache.org)
[![Slack](https://img.shields.io/badge/Join_Slack-e01d5a)](https://slack.grails.org/)
[![GitHub Discussions](https://img.shields.io/github/discussions/apache/grails-website)](https://github.com/apache/grails-website/discussions)

---

## Introduction

This repository is the **consolidated home for the Apache Grails website**:  
https://grails.apache.org/

It contains:

- Current and legacy documentation
- Guides and learning resources
- Grails Forge–related content
- Website source code and configuration

Content from multiple Grails repositories is aggregated here and published to  
https://grails.apache.org/ using the `publish` process defined in `.asf.yml`.

For information about using the Grails framework itself, please refer to the  
[Apache Grails Documentation](https://grails.apache.org/docs/).

---

## Purpose of This Repository

The `grails-website` repository is responsible for:

- Maintaining the official Apache Grails website
- Managing documentation and guides
- Aggregating website content from different repositories
- Publishing the site using Apache infrastructure

This repository **does not contain the Grails framework source code**.

---

## Repository Structure

Below is a high-level overview of the repository to help new contributors
understand how it is organised:

```text
grails-website/
├── src/                # Website source code
├── content/            # Documentation and guides
├── assets/             # Static assets (CSS, JavaScript, images)
├── config/             # Website configuration
├── .asf.yml            # Apache site publishing configuration
├── build.gradle        # Build configuration
└── README.md           # Project documentation
```

You do not need to understand every directory to get started—this overview
is provided to help you get oriented.

## Prerequisites
To work on the Apache Grails website locally, you will need:
- Java Development Kit (JDK)
- Git
- Gradle


## Getting Started (Local Setup)
Follow the steps below to run the Grails website locally.

1. Clone the repository
   `git clone https://github.com/apache/grails-website.git
cd grails-website`

2. Build the project
   `./gradlew build
`

3. Run the website locally
   `./gradlew bootRun
`

4. Open the website
   `http://localhost:8080
`

## Optional: Installing Grails Using SDKMAN!
If you prefer managing Grails versions locally, you can install Grails using
[https://sdkman.io/](SDKMAN!)

Install SDKMAN!
`curl -s https://get.sdkman.io | bash`

Initialise SDKMAN!:
`source "$HOME/.sdkman/bin/sdkman-init.sh"`

Verify installation:
`sdk version`

Install Grails
`sdk install grails`

Verify Grails installation:
`grails --version`

|Note: Installing Grails is optional for working on the website itself, but may
be useful when contributing to Grails-related tools or documentation.|




