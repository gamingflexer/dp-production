<?php
  $file_name =  $_FILES['file']['name'];
  $tmp_name = $_FILES['file']['tmp_name'];
  $file_up_name = time().$file_name;
  move_uploaded_file($tmp_name, "{{ url_for('static', filename='files')".$file_up_name);
?>