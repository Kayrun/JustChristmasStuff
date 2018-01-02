#!/usr/bin/perl -w

#Use the DBI (database interface) module
use DBI;

#Declare variables with MySQL connection data
$db="int420_173a30";
$user="int420_173a30";

$passwd="ebTA9338";
$host="db-mysql.zenit";
$connectionInfo="dbi:mysql:$db;$host";

#Print HTTP header
print "Content-Type:text/html\n\n";

##If first time script runs (GET) display table of friends ####
if($ENV{REQUEST_METHOD} eq "GET")
 {
   &showcatalog;
   exit;
 }

else
    {
      &parseform;
      ## Test for value of submit button ##
      if($form{submit} eq "Add a Product")
          {
            &displayaddform;
          }
      elsif($form{submit} eq "Insert Product")
        {
          ## Test for valid data if true insert record, if false resend form ##
          if(&validatedata)
            {
              &insertproduct;
              &showcatalog;
            }
          else
            {
              &displayaddform;
            }
        }
      elsif($form{submit} eq "Delete")
        {
          &deleteproduct;
          &showcatalog;
        }
      elsif($form{submit} eq "Change")
        {
          &displaychangeform;
        }
      elsif($form{submit} eq "Update Product")
        {
          if(&validatedata)
            {
              &updateproduct;
              &showcatalog;
            }
          else
            {
          &displaychangeform;
         }
      }
  }


#sub for parsing form using POST method ##

sub parseform
  {
  read(STDIN,$qstring,$ENV{'CONTENT_LENGTH'}); #get data from environment variables
  @pairs = split(/&/, $qstring); #break data up on ampersands and store in array
  foreach (@pairs) {             #start a for loop to process form data
  ($key, $value) = split(/=/);   #split field name and value on '=', store in two scalar variables
    $value =~ tr/+/ /;                                           #translate + signs back to spaces
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("c", hex($1))/eg; # translate special characters
    $form{$key} = $value;
   }
  }
#sub for inserting new record into table ##

sub insertproduct
{
  #Form SQL insert statement
  $insert = qq~insert jcscatalog (Name, Description, Price, Image)
            values ('$form{name}','$form{description}','$form{price}', '$form{image}')~;

 #Connect to MySQL and create Database Handler $dbh
 $dbh=DBI->connect($connectionInfo,$user,$passwd);

 ## Prepare MySQL statement and create Statement Handler $sth ##

 $sth=$dbh->prepare($insert);

 ## execute select statement ##

 $sth->execute();

 #Disconnect Database
 $dbh->disconnect();
 }

 #Sub for deleting a product

sub deleteproduct
{
  #Form SQL delete Statement
  $delete = qq~delete from jcscatalog where ID = '$form{id}'~;

  #Connect to MySQL and create Database Handler $dbh
  $dbh=DBI->connect($connectionInfo,$user,$passwd);

  $sth=$dbh->prepare($delete);
  #Prepare MySQL statement and create Statement Handler $sth
  $sth->execute();

  $dbh->disconnect();
}

sub updateproduct
{
  #Form SQL Update Statement
  $update = qq~update jcscatalog set name = '$form{name}', Description = '$form{description}', Price = '$form{price}', Image = '$form{image}' where id = '$form{id}'~;
  #Connect to MySQL and create Database Handler $dbh
  $dbh=DBI->connect($connectionInfo,$user,$passwd);

  $sth=$dbh->prepare($update);
  #Prepare MySQL statement and create Statement Handler $sth
  $sth->execute();

  $dbh->disconnect();
}

 ## Sub for displaying all products in table form ##

 sub showcatalog
  {
    ## start HTML table ##
    print qq~<html>
    <head>
    <style>
    table {
        border-collapse: collapse;
        width: 100%;
    }

    th, td {
        text-align: left;
        padding: 8px;
    }

    tr:nth-child(even){background-color: #EE6363}

    th {
        background-color: #4CAF50;
        color: white;
    }
    input[type=button], input[type=submit], input[type=reset] {
      background-color: #4CAF50;
      border: none;
      color: white;
      padding: 16px 32px;
      text-decoration: none;
      margin: 4px 2px;
      cursor: pointer;
    }
    input[type=text], input[type=password] {
      width: 100%;
      padding: 12px 20px;
      margin: 8px 0;
      box-sizing: border-box;
      border: none;
      background-color: #4CAF50;
      color: white;
    }
    </style>
    <Title>Products Catalog</Title>
    </head>
    <body>
    <table border=1 >
    <tr>
    <th>ID</th><th>Name</th><th>Description</th>
    <th>Price(CAD)</th><th>Image</th>
    <th>Change Product</th>
    </tr>~;

## SQL select statement ##
$select = qq~select ID,Name, Description, Price, Image from jcscatalog~;

## Connect to MySQL and create Database Handler $dbh ##
$dbh=DBI->connect($connectionInfo,$user,$passwd);

## Prepare MySQL statement and create Statement Handler $sth ##

$sth=$dbh->prepare($select);

## execute select statement ##

$sth->execute();

##Loop through each record selected and print in html table ##
while(@row=$sth->fetchrow_array())
  {  $image=qq~<img src=http://zenit.senecacollege.ca:16782/images/$row[4] height=300 width=300>~;
    $id2=$row[0];
    print qq~<tr>
    <td>$row[0]</td><td>$row[1]</td><td>$row[2]</td>
    <td>$row[3]</td><td>$image</td>
    <td>
      <form action="jcscatalog.cgi" method="post">

        <input type="hidden" name="id" value="$id2">
        <input type="submit" name="submit" value="Delete">
        <input type="submit" name="submit" value="Change">
      </form>
      </td>
    </tr>~;
  }

  ## Close HTML table ##
  print qq~</table>
        <form action="jcscatalog.cgi" method="post">
        <input type="submit" name="submit" value="Add a Product">
        <br>
        </form>
        </body>
        </html>~;

  ## Disconnect from MySQL database ##
  $dbh->disconnect();

  }

sub displayaddform
  {
    print qq~
          <html>
          <head>
          <meta charset ="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
input[type=button], input[type=submit], input[type=reset] {
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 16px 32px;
  text-decoration: none;
  margin: 4px 2px;
  cursor: pointer;
}
input[type=text], input[type=password] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
  border: none;
  background-color: #4CAF50;
  color: white;
}
  </style>
          <title>Add a Product </title>
          </head>
          <body>

          <form action="jcscatalog.cgi" method="post">

          <center>
          <h2>Add a Product</h2>
          Product Name: <input type="text" name="name" value="$form{name}">$errors{name}
          <br>
          Product Description: <input type="text" name="description" value="$form{description}">$errors{description}
          <br>
          Price (CAD): <input type="text" name="price" value="$form{price}">$errors{price}
          <br>
          Image Name: <input type="text" name="image" value="$form{image}">$errors{image}
          <br>
          <input type="submit" name="submit" value="Insert Product">
          </form>
          </body>
          </html>
          ~;
  }

#sub for displaying a form for changing record in table
sub displaychangeform
   {
 ## SQL select statement ##
 $select = qq~select ID,Name, Description, Price, Image from jcscatalog where ID = '$form{id}'~;

 ## Connect to MySQL and create Database Handler $dbh ##
 $dbh=DBI->connect($connectionInfo,$user,$passwd);

 ## Prepare MySQL statement and create Statement Handler $sth ##

 $sth=$dbh->prepare($select);

 ## execute select statement ##

 $sth->execute();

 ##Loop through each record selected and print in html table ##
 @row=$sth->fetchrow_array();

$id = $row[0];
$name= $row[1];
$description = $row[2];
$price = $row[3];
$image = $row[4];

 # {  $image=qq~<img src=http://zenit.senecacollege.ca:16782/images/$row[4] height=300 width=300>~;
 #   print qq~<tr>
 #   <td>$row[0]</td><td>$row[1]</td><td>$row[2]</td>
 #   <td>$row[3]</td><td>$image</td>
 #   <td>
 #     <form action="jcscatalog.cgi" method="post">
 #       <input type="hidden" name="id" value=$row[0]>
 #       <input type="submit" name="submit" value="Delete">
 #       <input type="submit" name="submit" value="Change"
 #     </form>
 #     </td>
 #   </tr>~;
 # }
   ## Display form with data from row to be changed ##
   print qq~<html>
   <head>
   <title>Update the Catalog</title>
   </head>
   <style>
   input[type=button], input[type=submit], input[type=reset] {
     background-color: #4CAF50;
     border: none;
     color: white;
     padding: 16px 32px;
     text-decoration: none;
     margin: 4px 2px;
     cursor: pointer;
   }
   input[type=text], input[type=password] {
     width: 100%;
     padding: 12px 20px;
     margin: 8px 0;
     box-sizing: border-box;
     border: none;
     background-color: #4CAF50;
     color: white;
   }
   </style>
          <body>
         <form action="jcscatalog.cgi" method="post">
         <center>
         <h2>Update the Catalog</h2>
         Product Name: <input type="text" name="name" value="$name">$errors{name}
         <br>
         Product Description: <input type="text" name="description" value="$description">$errors{description}
         <br>
         Price (CAD): <input type="text" name="price" value="$price">$errors{price}
         <br>
         Image Name: <input type="text" name="image" value="$image">$errors{image}
         <br>
         <input type="hidden" name="id" value="$id">
         <input type="submit" name="submit" value="Update Product">
         <br>
         </form>
         </body>
         </html>~;

   ## Disconnect from MySQL database ##
   $dbh->disconnect();

   }


## Sub for validating data before insert ##
sub validatedata
  {

    $valid = 1;
    foreach(keys %form)
    {
      if($form{$_} eq "")
        {
          $errormsg="Please enter valid data for required field";
          $valid = 0;
        }
      else
        {
          $errormsg="";
        }
      $errors{$_}=$errormsg;
    }

  #Test for a product name between 2 and 30 alphanumerics

              if($form{'name'} !~ /^[A-Za-z0-9 ]{2,30}$/)
                {
                  $errors{'name'} = "Please enter up to 30 characters Product name";
                  $valid = 0;
                }
              else #test for existing username in table
                {
           $select = qq~select Name from jcscatalog where name = '$form{name}'~;
           $dbh=DBI->connect($connectionInfo,$user,$passwd);
           $sth=$dbh->prepare($select);
           $sth->execute();

           if(@row=$sth->fetchrow_array())
               {
                   $errors{'name'} = "The product already exists!";
                   $missing = 0;
               }
             }
#Test for a product description between 2 and 250 alphanumerics

              if($form{'description'} !~ /^[A-Za-z0-9.-_ ]{2,250}$/)
                {
                 $errors{'description'} = "Please enter up to 250 characters Product Description";
                 $valid = 0;
                }

#Test for a price between 2 and 30 alphanumerics

              if($form{'price'} !~ /^\$?\d{0,8}(\.\d{1,4})?$/)
                {
                  $errors{'price'} = "Please enter a valid price";
                  $valid = 0;
                }

#Test for a .jpg or jpeg between 1 and 50 alphanumerics

            if($form{'image'} !~ /^([a-zA-Z0-9_%-]{1,45}+\.(?:jpeg|jpg|png))*$/)
                {
                  $errors{'image'} = "Please enter a valid .jpg or .jpeg image file name";
                  $valid = 0;
                }

  return $valid;
  }
