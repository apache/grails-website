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

- The Apache Grails Website
- Current documentation
- Legacy (pre-asf) documentation

It will also eventually contain the following, once they are migrated from the historical gh-pages grails.org subdomains:

- Grails Guides
- Grails Forge

Content from multiple Grails repositories is aggregated here and published to  
https://grails.apache.org/ using the `publish` process defined in `.asf.yml`.

For information about using the Grails framework itself, please refer to the  
[Apache Grails Documentation](https://grails.apache.org/docs/).

---

## Purpose of This Repository

The `grails-website` repository is responsible for:

- Aggregating website content from different repositories
- Publishing the site using Apache infrastructure

This repository **does not contain the Grails framework source code**.

---

## Repository Structure

Below is a high-level overview of the repository to help new contributors
understand how it is organised:

```text
grails-website/
├── docs-legacy-*/                     # Histoical Grails documentation prior to the move to ASF
├── docs/                              # Grails documentation including groovydocs - published from https://github.com/apache/grails-core/tree/HEAD/grails-doc
├── AddMatomoAnalytics.groovy          # Adds missing Apache Analytics Tracking run as `groovy AddMatomoAnalytics.groovy`
├── .asf.yml            # Apache site publishing configuration
└── README.md           # Project documentation
```

The remaining directories are all generated and published from https://github.com/apache/grails-static-website
