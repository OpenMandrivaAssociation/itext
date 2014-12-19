#!/bin/bash

#if [ $# -ne 1 ]; then
#    echo "Usage: ./create-sources VERSION"
#    exit 1
#fi

VERSION=${1}
TRVERSION=$( echo ${VERSION} | tr . _ )
NAME="itext"

svn export http://svn.code.sf.net/p/${NAME}/code/tags/iText_${TRVERSION} ${NAME}-temp/

find ./${NAME}-temp -name "*.jar" -delete
find ./${NAME}-temp -name "*.class" -delete

# Remove unused files
rm -Rf ./${NAME}-temp/src/jnlp
rm -Rf ./${NAME}-temp/.keywords
rm -Rf ./${NAME}-temp/lib
rm -Rf ./${NAME}-temp/test
rm -Rf ./${NAME}-temp/www

cd ./${NAME}-temp
tar cJf ../${NAME}-${VERSION}.tar.xz ./src