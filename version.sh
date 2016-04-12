#!/bin/bash

VERSION=dev
if test "${TRAVIS_PULL_REQUEST}" = "false"; then
    if test "${TRAVIS_TAG}" != ""; then
        VERSION=${TRAVIS_TAG}
    else
        if test "${TRAVIS_BRANCH}" != ""; then
            if test "${TRAVIS_BRANCH}" = "master"; then
                VERSION=latest
            else
                TMP_VERSION=`echo ${TRAVIS_BRANCH} |awk -F '.' '{print $1;}'`
                N=`echo ${TMP_VERSION} |grep '^[0-9][0-9]*$' |wc -l`
                if test ${N} -gt 0; then
                    VERSION="V${TMP_VERSION}"
                fi
            fi
        fi
    fi
fi

echo ${VERSION}
