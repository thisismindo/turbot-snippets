#!/bin/bash

rabbitmqctl add_user username password || echo "User 'username' already exists"

rabbitmqctl set_user_tags username administrator

rabbitmqctl set_permissions -p / username ".*" ".*" ".*"

echo "RabbitMQ user 'username' created successfully!"
