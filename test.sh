#!/bin/bash

mkdir -p testdir

touch ./testdir/taxes.txt
touch ./testdir/social_security_number.txt
touch ./testdir/homework.py
touch ./testdir/medical_report.pdf
touch ./testdir/diary.md
touch ./testdir/love_letter.docx
touch ./testdir/important_email.txt
touch ./testdir/test_answers.zip
touch ./testdir/system32.dll
touch ./testdir/receipt.txt
touch ./testdir/DO_NOT_DELETE.TXT
touch ./testdir/family_photos.zip
touch ./testdir/last_will_and_testament.pdf

python3 burn_directory.py testdir --burn-it
