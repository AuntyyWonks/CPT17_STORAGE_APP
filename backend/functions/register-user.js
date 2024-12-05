const AWS = require('aws-sdk');
const bcrypt = require('bcryptjs');
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const requestBody = JSON.parse(event.body);
    const { first_name, last_name, email, password, confirm_password, phone } = requestBody;

    // Validate passwords match
    if (password !== confirm_password) {
        return {
            statusCode: 400,
            body: JSON.stringify({ message: "Passwords do not match" }),
        };
    }

    // Hash the password
    const hashedPassword = await bcrypt.hash(password, 10);

    const params = {
        TableName: "Users",
        Item: {
            email,
            first_name,
            last_name,
            password: hashedPassword,
            phone_number,
        },
    };

    try {
        await dynamoDB.put(params).promise();
        return {
            statusCode: 201,
            body: JSON.stringify({ message: "User registered successfully!" }),
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ message: "Error registering user", error: error.message }),
        };
    }
};