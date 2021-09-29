#!/bin/bash


log_file="build_payments_images.log"

if [[ -f "$log_file"  ]] ; then
	rm "$log_file"
fi

# TODO change those 
images_payments_path="../css/images/pay"
destination_payments_path="../css/images/payments"

# if it does not exists create the directory otherwise no error
 mkdir -p $destination_payments_path

for x in $(ls $images_payments_path)
do
	full_path="${images_payments_path}/${x}"
	full_destination="${destination_payments_path}/${x}"

	# TODO if more flags are added change this to normal
	if [[ "$1" == "--log" ]] || [[ "$1" == "-l" ]]; then
		./build_image.py $full_path $full_destination >> $log_file
	else
		./build_image.py $full_path $full_destination
	fi

done
