// prob1.cc
// CPSC 2620 Assignment 4
// Briana Smith
// March 8, 2017
//
// This program allows the user to edit an empty line of text using the
// LineEditor class. The user can move the cursor left or right, and insert,
// delete, or change text based on cursor position or apply uppercase or
// lowercase to the whole line. Q to quit.


#include "lineEditor.h"
#include<iostream>
#include<string>

using namespace std;

char makeUpper(char c);
char makeLower(char c);

int main() {
   LineEditor myLine;
   char userIn, changeChar;
   string userString;
   
   cout<<myLine;

   do{
      cin>>userIn;

      //Moves cursor left
      if(userIn == 'L')
	 myLine.left();

      //Moves cursor right
      else if(userIn == 'R')
	 myLine.right();

      //Inserts string at cursor
      else if(userIn == 'I')
      {
	 cout<<"Enter string to insert: "<<endl;
	 cin>>userString;
	 myLine.insert(userString);
	 //cout<<myLine;
      }

      //Deletes char at cursor
      else if(userIn == 'D')
	 myLine.erase();

      //Changes char at cursor to user entry
      else if(userIn == 'C')
      {
	 cout<<"Enter new character: "<<endl;
	 cin>>changeChar;
	 myLine.change(changeChar);
      }

      //Makes entire line uppercase
      else if(userIn == 'U')
	 myLine.apply(makeUpper);

      //Makes entire line lowercase
      else if(userIn == 'l')
	 myLine.apply(makeLower);

      //Prints line to screen
      else if(userIn == 'P')
	 cout<<myLine;
   }
   //User enters Q to quit
   while(userIn!='Q');

   return 0;
}

//Function to make char uppercase
char makeUpper(char c)
{ return toupper(c);}

//Function to make char lowercase
char makeLower(char c)
{ return tolower(c);}
