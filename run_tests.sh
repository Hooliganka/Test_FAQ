#!/bin/bash

rm -rf allure-results/*

docker-compose up --build -d

docker-compose logs -f tests

TEST_EXIT_CODE=$(docker-compose ps -q tests | xargs docker inspect -f '{{.State.ExitCode}}')

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "Tests completed successfully!"
else
    echo "Tests failed with exit code $TEST_EXIT_CODE"
fi

echo "Allure report is available at http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html"