# Welcome to the MILO Preprocessor Repo
The preprocessing tool serves to prepare a dataset for MILO. This repo has all pieces of the tool avalable for exploration, tinkering and adaptation. The tool is build using Vue 3 (still with the vue CLI) and Vuetify for the frontend and Python and Flask for the backend. 

## Getting Started 
Given the rapidly changing nature of the underlying libraries as well as the complexity of getting the older version of numpy to work on Apple silicon, we've created a docker-compose file that will automatically run and reload the frontend and backend devopment services. The docker-compose file is also configured to build/run for the x64 architecture which is fully functional with Rosetta 2 on macOS.

## 1. Install docker and docker-compose 
[Follow the installation guide from docker's website or ask ChatGPT or Gemini for help](https://docs.docker.com/compose/install/)

## 2. Run docker compose
Navigate to your preprocessor directory with your terminal. If it is your first time running the composition, you'll need to build the images first.
```
docker compose build
```
Next start the servies.
```
docker compose up
```
If you would like to start them in detached mode to keep them running after you close your terminal
```
docker compose up -d
```

## 3. Review documentation
Review the MILO documentation for further specific questions on functionality. [https://milo-ml.com/docs/](https://milo-ml.com/docs/)




