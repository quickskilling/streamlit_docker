---
title: Streamlit Docker
emoji: 🐨
colorFrom: indigo
colorTo: red
sdk: docker
pinned: false
license: apache-2.0
app_port: 8501
---


## Introduction to Streamlit with Docker

## Overview

Location: Rexburg, Idaho When: July 16, 2024

This material uses [Polars](https://pola-rs.github.io/polars-book/user-guide/) and focuses [Streamlit](https://streamlit.io/) and dashboarding to introduce the data science app development process.

I am hosting this repo on [Github](https://github.com/quickskilling/streamlit_docker) and [Hugging Face](https://huggingface.co/spaces/ds460/docker_streamlit/tree/main).

## Installing the tools

We will need [Visual Studio Code](https://code.visualstudio.com/download) and [Python](https://www.python.org/downloads/) installed for this short course. Each tool has additional packages/extensions that we will need to install as well.

### Visual Studio Code Extensions

You can use [Managing Extensions in Visual Studio Code](https://code.visualstudio.com/docs/editor/extension-marketplace) to learn how to install extensions. We will use [Python - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension heavily. [Managing Extensions in Visual Studio Code](https://code.visualstudio.com/docs/editor/extension-marketplace) provides more background on extensions if needed.

## Repo Navigation

### `guides` folder

The `guides` folder has cheat sheets for polars and streamlit

### `scripts_build` folder

The `scripts_build` folder has the munging scripts that built the data for the app we will explore.

### Other key files

- The [slides.html](slides.html) is a Remark Slides presentation on Dashboarding.  You can read more at [remark_slides.md](remark_slides.md). The slides are embedded in the default Streamlit app for this repository.
- [Dockerfile](Dockerfile) is the build script for our Docker Image
- [docker-compose.yml](docker-compose.yml) provides an easy way to start our docker container.  [Docker Compose](https://docs.docker.com/compose/#:~:text=It%20is%20the%20key%20to,single%2C%20comprehensible%20YAML%20configuration%20file.) is _'the key to unlocking a streamlined and efficient development and deployment experience.'_
- [requirements.txt](requirements.txt) is run from the [Dockerfile](Dockerfile) and installs the needed Python packages.
- [README.md](README.md) is this file.  The `YAML` at the top is necessary for the Streamlit app to work correctly. Specifically the `app_port: 8501` is needed.  All other information can and should be manipulated.
- [streamlit.py] is our Streamlit app.
- The remaining files are data files. 

### Final notes

Here is how to sync a Github repo with Hugging face.

- [Sync with Github Actions](https://dev.to/0xkoji/sync-github-repo-and-hugging-face-space-repo-with-github-actions-3ca1)
