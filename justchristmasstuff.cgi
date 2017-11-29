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

#If first time script run display form
if($ENV{"REQUEST_METHOD"} eq "GET")
  {
    &displayform();
    exit;
  }

#Else process for and insert into DB
else  {
	&parseform();
    #print "<html><head><title>Student Survey</title></head>\n";
    #print "<body>\n";
    #print "Login Name:",             $form{"lname"}, "<br>";
    #print "Full Name:",       $form{"fname"}, "<br>";
    #print "Phone Number:",       $form{"phone"}, "<br>";
    #print "Email:",   $form{"email"}, "<br>";
    #print "</body></html>\n"; */
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
    #Form SQL insert statement
    $insert = qq~insert jcsaccounts(lname, passkey, phone, email, firstname, lastname, streetaddress, city, postalcode, province) values('$form{lname}','$form{passkey}','$form{phone}','$form{email}', '$form{firstname}', '$form{lastname}', '$form{streetaddress}', '$form{city}', '$form{postalcode}', '$form{province}')~;
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
              <p>Login Name: <input type="text" name="lname" value="$form{lname}">$errors{lname}</p>
              <p>Password: <input type="password" name="passkey" value="$form{passkey}">$errors{passkey}<p>
              <p>First Name: <input type="text" name="firstname" value="$form{firstname}">$errors{firstname}<p>
              <p>Last Name: <input type="text" name="lastname" value="$form{lastname}">$errors{lastname}<p>
              <p>Street Address: <input type="text" name="streetaddress" value="$form{streetaddress}">$errors{streetaddress}<p>
              <p>City: <input type="text" name="city" value="$form{city}">$errors{city}<p>
              <p>Postal Code: <input type="text" name="postalcode" value="$form{postalcode}">$errors{postalcode}<p>
              <p>Province: <input type="text" name="province" value="$form{province}">$errors{province}<p>
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
          if($missing == 1)
            {
              &displayform;
              exit;
            }
        }
