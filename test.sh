#!/usr/bin/env bash

### Costants

MYSQL_TEST_DB_NAME="meal_planner_test"
MYSQL_TEST_USER="root"
MYSQL_TEST_PASSWORD=""
UNIT_TEST_FLAG="U"
FUNCTIONAL_TEST_FLAG="F"
INTEGRATION_TEST_FLAG="I"
ENABLED_TESTS=""
TEST_DIR="tests/"
UNIT_TEST_DIR="$TEST_DIR""unit"
UNIT_TEST_COVERAGE_SOURCE="app/models"
FUNCTIONAL_TEST_DIR="$TEST_DIR""functional"
FUNCTIONAL_TEST_COVERAGE_SOURCE="app/controllers,app/dao"
INTEGRATION_TEST_DIR="$TEST_DIR""integration"
#TODO: Abstract out integration points and set as its own source
INTEGRATION_TEST_COVERAGE_SOURCE="$UNIT_TEST_COVERAGE_SOURCE,$FUNCTIONAL_TEST_COVERAGE_SOURCE"
DISTINCTIVELY_RUN_TESTS=false
COVERAGE_REPORT_ENABLED=true
COVERAGE_SOURCE=""
DIRS_TO_TEST=""

### ----------
### Functions
### ----------

# Argument Processing

arg_is_flag ()
{
    if [[ $1 == "-"* ]]; then
        return 0 # 0 = true
    else
        return 1 # 1 = false
    fi
}

enable_test ()
{
    NEW_TEST=$1
    if [[ $ENABLED_TESTS != *$NEW_TEST* ]]; then
        ENABLED_TESTS+=$NEW_TEST
    fi
}

process_flag()
{
    flag="$1"
    #check each letter in flag
    for i in $(seq 1 ${#flag})
    do
        test_flag=${flag:i-1:1}
        case "$test_flag" in
            h|H)
                echo "   Usage: ./test.sh -flags"
                echo "   -h|H: prints test script help"
                echo "   -p: requests database password"
                echo "   -u: requests database user"
                echo "   -n: requests database name"
                echo "   -U: performs unit tests (default)"
                echo "   -F: performs functional tests (default)"
                echo "   -I: performs integration tests"
                echo "   -a|A: performs all test suites"
                echo "   -s|S: silence coverage reporting"
                echo "   -d|D: distinctively perform each test suite"
                exit 0
                ;;
            p)
                request_db_password
                ;;
            u)
                request_db_user
                ;;
            n)
                request_db_name
                ;;
            "$UNIT_TEST_FLAG")
                enable_test "$UNIT_TEST_FLAG"
                ;;
            "$FUNCTIONAL_TEST_FLAG")
                enable_test "$FUNCTIONAL_TEST_FLAG"
                ;;
            "$INTEGRATION_TEST_FLAG")
                enable_test "$INTEGRATION_TEST_FLAG"
                ;;
            a|A)
                enable_test "$UNIT_TEST_FLAG"
                enable_test "$FUNCTIONAL_TEST_FLAG"
                enable_test "$INTEGRATION_TEST_FLAG"
                ;;
            s|S)
                echo "Coverage reporting disabled..."
                COVERAGE_REPORT_ENABLED=false
                ;;
            d|D)
                echo "Running test suites distinctively enabled..."
                DISTINCTIVELY_RUN_TESTS=true
                ;;

        esac
    done
}

process_args ()
{
    for flag in "$@"
    do
        if arg_is_flag $flag; then
            process_flag $flag
        fi
    done
}

# Info Requests

request_db_password ()
{
    printf "Enter test db password:\n"
    read -s MYSQL_TEST_PASSWORD
    MYSQL_TEST_PASSWORD="-p$MYSQL_TEST_PASSWORD"
}

request_db_name()
{
    read -p "Enter test db name: [$MYSQL_TEST_DB_NAME]" MYSQL_TEST_DB_NAME
    MYSQL_TEST_DB_NAME=${MYSQL_TEST_DB_NAME:-$MYSQL_TEST_DB_NAME_DEF}
}

request_db_user ()
{
    read -p "Enter test db user: [$MYSQL_TEST_USER]" MYSQL_TEST_USER
    MYSQL_TEST_USER=${MYSQL_TEST_USER:-$MYSQL_TEST_USER_DEF}
}

# Setup

set_default_test_suites_if_not_specified (){
    if [[ ${#ENABLED_TESTS} == "0" ]]; then
        echo "Enabling default test suites..."
        enable_test $UNIT_TEST_FLAG
        enable_test $FUNCTIONAL_TEST_FLAG
    fi
}

start_mysql_server ()
{
    LIST=$(mysql.server status)
    SOURCE="SUCCESS!"
    if echo "$LIST" | grep -vq "$SOURCE"; then
        echo "MySQL not running. Starting now...";
        mysql.server start;
    fi
}

install_coverage_tool ()
{
    COVERAGE=$(pip list --format=columns)
    COVERAGE_SOURCE="coverage"
    if [[ $COVERAGE != *$COVERAGE_SOURCE* ]]; then
        printf "\nInstalling coverage package...\n"
        pip install coverage
    fi
}

create_test_db ()
{
    echo "Creating test db..."
    mysql -u $MYSQL_TEST_USER $MYSQL_TEST_PASSWORD -e "CREATE DATABASE $MYSQL_TEST_DB_NAME"
}

setup ()
{

    set_default_test_suites_if_not_specified

    if "$COVERAGE_REPORT_ENABLED"; then
        install_coverage_tool
    fi

    if [[ $ENABLED_TESTS == *"$FUNCTIONAL_TEST_FLAG"* ]] ||
    [[ $ENABLED_TESTS  == *"$INTEGRATION_TEST_FLAG"* ]] ; then
        start_mysql_server
        create_test_db
    fi
}

# Test

google_cloud_dir ()
{
    DIR="$(which gcloud)"
    DIR=$(dirname "$DIR")
    DIR=$(dirname "$DIR")
    echo "$DIR"
}

run_test ()
{
    COVERAGE_SOURCE="$1"
    TEST_PATH="$2"
    GOOGLE_CLOUD_DIR=$(google_cloud_dir)
    TEST_RUNNER_CMD="runner.py '$GOOGLE_CLOUD_DIR' --test-path  $TEST_PATH"
    if "$COVERAGE_REPORT_ENABLED"; then
        eval "coverage run -p --source=$COVERAGE_SOURCE $TEST_RUNNER_CMD"
    else
        eval "python $TEST_RUNNER_CMD"
    fi

}

append_option ()
{
    SOURCE_OPTION=$1
    if [[ ${#COVERAGE_SOURCE} == "0" ]]; then
        COVERAGE_SOURCE="$SOURCE_OPTION"
    else
        COVERAGE_SOURCE+=,"$SOURCE_OPTION"
    fi

    DIR_OPTION=$2
    if [[ ${#DIRS_TO_TEST} == "0" ]]; then
        DIRS_TO_TEST="$DIR_OPTION"
    else
        DIRS_TO_TEST+=,"$DIR_OPTION"
    fi
}

run_enabled_tests ()
{
    local COVERAGE_SOURCE=""
    local TEST_DIRS=""
    for i in $(seq 1 ${#ENABLED_TESTS})
    do
        test_flag=${ENABLED_TESTS:i-1:1}
        case "$test_flag" in
            "$UNIT_TEST_FLAG")
                append_option "$UNIT_TEST_COVERAGE_SOURCE" "$UNIT_TEST_DIR"
                ;;
            "$FUNCTIONAL_TEST_FLAG")
                append_option "$FUNCTIONAL_TEST_COVERAGE_SOURCE" "$FUNCTIONAL_TEST_DIR"
                ;;
            "$INTEGRATION_TEST_FLAG")
                append_option "$INTEGRATION_TEST_COVERAGE_SOURCE" "$INTEGRATION_TEST_DIR"
                ;;
        esac
    done
    run_test "$COVERAGE_SOURCE" "$DIRS_TO_TEST"
}

run_enabled_tests_distinctively ()
{
    for i in $(seq 1 ${#ENABLED_TESTS})
    do
        test_flag=${ENABLED_TESTS:i-1:1}
        case "$test_flag" in
            "$UNIT_TEST_FLAG")
                printf "\nUnit Testing:\n"
                run_test "$UNIT_TEST_COVERAGE_SOURCE" "$UNIT_TEST_DIR"
                ;;
            "$FUNCTIONAL_TEST_FLAG")
                printf "\nFunctional Testing:\n"
                run_test "$FUNCTIONAL_TEST_COVERAGE_SOURCE" "$FUNCTIONAL_TEST_DIR"
                ;;
            "$INTEGRATION_TEST_FLAG")
                printf "\nIntegration Testing:\n"
                run_test "$INTEGRATION_TEST_COVERAGE_SOURCE" "$INTEGRATION_TEST_DIR"
                ;;
        esac
    done
}

print_coverage ()
{
    printf "\nCode Coverage:\n"
    coverage combine
    coverage report -m
}

test_and_report ()
{

    if "$DISTINCTIVELY_RUN_TESTS"; then
        run_enabled_tests_distinctively
    else
        run_enabled_tests
    fi

    if "$COVERAGE_REPORT_ENABLED"; then
        print_coverage
    fi
}

# Teardown

delete_test_db ()
{
    echo "Deleting test db..."
    mysql -u $MYSQL_TEST_USER $MYSQL_TEST_PASSWORD -e "DROP DATABASE $MYSQL_TEST_DB_NAME"
}

create_space_between_tests ()
{
    printf "\n\n"
}

teardown ()
{
    if [[ $ENABLED_TESTS  == *"$FUNCTIONAL_TEST_FLAG"* ]] ||
    [[ $ENABLED_TESTS  == *"$INTEGRATION_TEST_FLAG"* ]] ; then
        delete_test_db
    fi
    create_space_between_tests
}

### ----------
### Main
### ----------

process_args "$@"
setup
test_and_report
teardown
