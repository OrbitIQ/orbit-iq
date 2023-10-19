# orbitiq


## invite object

```json
{
  "userId": "string",
  "timestamp": "<unix-timestamp>"
}
```

## **Requests**

|            Route             |        Description        |
| :--------------------------: | :-----------------------: |
| [GET /orbitiq](#get-orbit-user) | return lastest data |
[POST /orbitiq](#post-orbit-user) | post edited data |
---

## **GET /orbit/users**


- **Query**

  - 

- **Headers**  
  None
- **Cookie**  
  

- **Success Response:**

  - **Code:** 200
    - **Content:**
    ```json
    {
     
    }
       ```

- **Error Responses:**
  - **Code:** 401
    - **Content:**
    ```json
    {
      "statusCode": 401,
      "error": "Unauthorized",
      "message": "."
    }
    ```
  - **Code:** 403

    - **Content:**
      ```json
      {
        "message": "."
      }
      ```
    - **Code:** 404

    - **Content:**
      ```json
      {
        "message": "User not found."
      }
      ```
  - **Code:** 500
    - **Content:**
    ```json
    {
      "statusCode": 500,
      "error": "",
      "message": ""
    }
    ```

## **POST /orbitiq/user**



- **Params**\
    None
- **Query**\
    None
- **Body**\
   
- **Headers**\
    None
- **Cookie**\
    None
- **Success Response:**
    - **Code:** 201
        - **Content:** 
        ```json
       {
        
       }
      ```
  - **Code:** 401
    - **Content:**
      ```json
        { 
          
        }
      ```
  - **Code:** 404
    - **Content:**
      ```json
        { 
          
        }
      ```
  - **Code:** 409
    - **Content:**
      ```json
        { 
        
        }
      ```

- **Error Response:**
    - **Code:** 500
        - **Content:**
          ```json
           { 
             "statusCode": 500,
             "error": "", 
             "message": "" 
           }
      ```