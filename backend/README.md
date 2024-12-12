# Self-Storage Unit Booking System

## Project Overview
This project is a cloud-based application that allows customers to book and manage self-storage units. It includes a secure backend API, a static-hosted web app, and optional functionality for sending fake invoices. The project leverages various AWS services for authentication, data storage, and hosting.

---

## Features

### Backend
- **Authentication**: Users must register and authenticate using AWS Cognito.
- **API Endpoints**:
  - `POST /bookUnit`: Book a storage unit.
  - `GET /listUnits`: Retrieve available storage units.
  - `PUT /updateBooking`: Update an existing booking.
  - `DELETE /cancelBooking`: Cancel a booking.
- **Data Storage**: All booking and unit data is stored in AWS DynamoDB.
- **Infrastructure Deployment**: Managed using AWS CloudFormation, SAM, or CDK.

### Frontend
- **Static Web Application**:
  - Users can view available units, make bookings, and manage their reservations.
  - Integrated with AWS Cognito using Amplify SDK for secure login and registration.
- **Hosting**:
  - Deployed as a static site on AWS S3.
  - Distributed globally using AWS CloudFront.


## Architecture

### Deployment Diagram
The system is composed of the following:
1. **Frontend**: Hosted on **S3**, distributed via **CloudFront**.
2. **Backend**:
   - **API Gateway**: Hosts the API endpoints.
   - **Cognito**: Manages authentication.
   - **Lambda Functions**: Handle API requests.
   - **DynamoDB**: Stores application data.
---

## Getting Started

### Prerequisites
- AWS Account
- AWS CLI configured
- Node.js installed

### Deployment Steps

#### Backend
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd backend
   ```
2. Build and Deploy the backend infrastructure:
   ```bash
   sam build --use-container
   sam deploy --guided
   ```
3. Note the API Gateway endpoint and Cognito User Pool details from the output.

#### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Deploy the web app:
   ```bash
   s3
   ```
4. Configure S3 and CloudFront using SAM or CDK if not using Amplify.


## Testing

### API Testing
1. Use **Postman** to test the API endpoints.
2. Authenticate using a Cognito token:
   - Register users in Cognito.
   - Obtain a token using a bash script or Postman.
   - Include the token in the `Authorization` header.

### Web App
1. Access the deployed web app via the CloudFront URL.
2. Test login, booking, and management functionality.


## Technologies Used

### AWS Services
- **Cognito**: User authentication.
- **API Gateway**: API management.
- **Lambda**: Serverless compute.
- **DynamoDB**: Data storage.
- **S3**: Static website hosting.
- **CloudFront**: Global content distribution.

### Tools
- **Infrastructure-as-Code**: CloudFormation, SAM, CDK.
- **Frontend**: HTML CSS JavaScript.
- **Testing**: Postman.

---

