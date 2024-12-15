# ba-kunder

## Overview

This README provides the necessary information to set up, configure, and use the microservice. It includes details about environmental variables, API endpoints, and dependencies.

The service can be accesed here: https://ba-kunder-auc6hdhuejg4hnfr.northeurope-01.azurewebsites.net/apidocs


---

## Environmental Variables

The microservice requires the following environmental variables to be configured before running. Ensure these variables are set correctly in your environment.

| Variable  | Required | Default | Description                |
| --------- | -------- | ------- | -------------------------- |
| `DB_PATH` | Yes      | None    | Path to the database file. |

---

## API Endpoints

Below is a list of the API endpoints exposed by this microservice. Each endpoint includes the HTTP method, a brief description, possible status codes, and the returned data.

### Endpoints

| Path             | Method | Description                          | Status Codes   | Response                                                                                     |
|------------------|--------|--------------------------------------|----------------|---------------------------------------------------------------------------------------------|
| `/kunder`        | POST   | Create a new customer                | 201, 400       | Object with `cpr`, `navn`, `tlf`, `email`, and `adresse` or error message explaining failure.|
| `/kunder/<cpr>`  | GET    | Retrieve a specific customer by CPR  | 200, 400, 404  | Object with `cpr`, `navn`, `tlf`, `email`, `adresse` or error message explaining failure.    |
| `/kunder`        | GET    | Retrieve a list of customers         | 200, 404       | Array of objects each containing `cpr`, `navn`, `tlf`, `email`, and `adresse` or error message explaining failure.|


---

## Dependencies

The following dependencies are required to run the microservice. These are specified in the `requirements.txt` file.

---
