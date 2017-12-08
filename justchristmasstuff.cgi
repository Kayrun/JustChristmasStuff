#!/usr/bin/perl -wT

#Use the DBI (database interface) module
use DBI;

use Digest::SHA1 qw(sha1_hex sha1_base64); #encryption digest

#Declare variables with MySQL connection data
$db="int420_173a30";
$user="int420_173a30";

$passwd="ebTA9338";
$host="db-mysql.zenit";
$connectionInfo="dbi:mysql:$db;$host";

#Print HTTP header
print "Content-Type:text/html\n\n";

#If first time script run display form
if($ENV{"REQUEST_METHOD"} eq "GET")
  {
    &displayform();
    exit;
  }

#Else process for and insert into DB
else  {
	  &parseform();
    &verifyform();
    &insertfriend();
    exit;
}

#Standard form parsing using POST method
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

sub insertfriend
  {

    $cryptpasswd = sha1_base64($form{passkey}); #encrypting the password

    #Form SQL insert statement
    $insert = qq~insert jcsaccounts(lname, passkey, phone, email, firstname, lastname, streetaddress, city, postalcode, province) values('$form{lname}','$cryptpasswd','$form{phone}','$form{email}', '$form{firstname}', '$form{lastname}', '$form{streetaddress}', '$form{city}', '$form{postalcode}', '$form{province}')~;
    $dbh=DBI->connect($connectionInfo,$user,$passwd);

  #Prepare MySQL statement and create Statement Handler $sth
  $sth=$dbh->prepare($insert);

  #Execute Statement Handler and test for success
  if($sth->execute())
      {
          &displaysuccess;
      }
  else
      {
          &displayfail;
      }

  #Disconnect the database connection
  $dbh->disconnect();
}

sub displaysuccess
  {
   print qq~<html>
            <head>
            <title>Account Creation</title>
            </head>
            <body>
	    <center>
            <h2>Acount Created Successfully!</h2>
            <img src="http://www.clker.com/cliparts/2/k/n/l/C/Q/transparent-green-checkmark-hi.png" alt="Accepted" width="460" height="345">
	    </body>
            </html>
            ~;
    }

  sub displayfail
    {
      print qq~<html>
               <head>
               <title>Account Creation</title>
               </head>
               <body>
               <h2>Uh oh, account creation failed</h2>
               </body>
               </html>
               ~;
    }

    sub displayform
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
	      <title>Just Christmas Stuff</title>
              </head>
              <body bgcolor="#EE6363">
              <form action="justchristmasstuff.cgi" method="POST">
              <center>
	      <h1>Just Christmas Stuff</h1>
	      </center>
		<h2>Registration</h2>
              <p>Login Name (2 to 8 characters): <input type="text" name="lname" value="$form{lname}">$errors{lname}</p>
              <p>Password ( 6 to 10 characters): <input type="password" name="passkey" value="$form{passkey}">$errors{passkey}<p>
              <p>Retype Password: <input type="password" name="passkey2" value="$form{passkey2}">$errors{passkey2}<p>
              <p>First Name: <input type="text" name="firstname" value="$form{firstname}">$errors{firstname}<p>
              <p>Last Name: <input type="text" name="lastname" value="$form{lastname}">$errors{lastname}<p>
              <p>Street Address: <input type="text" name="streetaddress" value="$form{streetaddress}">$errors{streetaddress}<p>
              <p>City: <input type="text" name="city" value="$form{city}">$errors{city}<p>
              <p>Postal Code: <input type="text" name="postalcode" value="$form{postalcode}">$errors{postalcode}<p>
              <p>Province (eg. ON,AB,PE,QC etc.): <input type="text" name="province" value="$form{province}">$errors{province}<p>
              <p>Phone Number: <input type="text" name="phone" value="$form{phone}">$errors{phone}</p>
              <p>E-mail: <input type="text" name="email" value="$form{email}">$errors{email}</p>
              <input type="submit" value="Insert" name="Insert"/>
              <input type="reset" value="Reset" name="reset"/>
              </form>
              </body>
              </html>
              ~;
      }

      sub verifyform
        {
          $missing = 0;         #assuming there is nothing missing and hence initializing it to 0

          foreach (keys %form)
            {
              if($form{$_} eq "")
                {
                  $errormsg="Please enter data for required field";
                  $missing = 1; #If there is a missing field, setting the flag to 1
                }
              else
                {
                  $errormsg="";
                }
              $errors{$_}=$errormsg;   #Load the % errors hash with error message
            }

          #Test for username between 2 and 8 alphanumerics

          if($form{'lname'} !~ /^[a-z0-p]{2,8}$/)
            {
              $errors{'lname'} = "Please enter up to 8 character alphanumeric username";
              $missing = 1;
            }
          else #test for existing username in table
            {
              $select = qq~select lname from jcsaccounts where lname = '$form{lname}'~;
              $dbh=DBI->connect($connectionInfo,$user,$passwd);
              $sth=$dbh->prepare($select);
              $sth->execute();

              if(@row=$sth->fetchrow_array())
                  {
                      $errors{'lname'} = "Name already registered";
                      $missing = 1;
                  }
                }
            #Test for password between 6 and 10 alphanumerics
            if($form{'passkey'} !~ /^[a-z0-9A-Z]{6,10}$/)
              {
                $errors{'passkey'} = "Enter 6 to 10 character password";
                $missing = 1;
              }

            #Test for password entered twice
            if ($form{'passkey'} ne $form{'passkey2'})
              {
                $errors{'passkey2'} = "Passwords don't match";
                $missing = 1;
              }

          #Test for Postal Code (Canadian)
          if($form{'postalcode'} !~ /^([ABCEGHJKLMNPRSTVXY][0-9][A-Z] [0-9][A-Z][0-9])*$/)
            {
              $errors{'postalcode'} = "Not a valid Postal Code";
              $missing = 1;
            }

          #Test for city between 1 and 50 alphabets
            if($form{'city'} !~ /^[a-zA-Z ]{1,50}$/)
              {
                $errors{'city'} = "Not a valid City";
                $missing = 1;
              }

          #Test for streetaddress between 1 and 100 alphanumerics
                if($form{'streetaddress'} !~ /^[a-zA-Z0-9 ]{1,100}$/)
                  {
                    $errors{'streetaddress'} = "Please enter a valid street address";
                    $missing = 1;
                  }

          #Test for firstname between 1 and 25 alphabets
                    if($form{'firstname'} !~ /^[a-zA-Z]{1,25}$/)
                      {
                        $errors{'firstname'} = "Please enter a shorter name";
                        $missing = 1;
                      }

          #Test for lastname between 1 and 25 alphabets
                   if($form{'lastname'} !~ /^[a-zA-Z]{1,25}$/)
                      {
                        $errors{'lastname'} = "Please enter a shorter name";
                        $missing = 1;
                      }

          #Test for Email Addresses

          if($form{'email'} !~ /^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})*$/)
            {
              $errors{'email'} = "Not a valid E-mail address";
              $missing = 1;
            }

            #Test for Phone Numbers

            if($form{'phone'} !~ /^((([0-9]{1})*[- .(]*([0-9]{3})[- .)]*[0-9]{3}[- .]*[0-9]{4})+)*$/)
              {
                $errors{'phone'} = "Not a valid Phone Number";
                $missing = 1;
              }

        #Test for Provinces

        if($form{'province'} !~ /^(?:AB|BC|MB|N[BLTSU]|ON|PE|QC|SK|YT)*$/)
          {
            $errors{'province'} = "Not a valid Province";
            $missing = 1;
          }

        if($missing == 1)
          {
            &displayform;
            exit;
          }
      }
