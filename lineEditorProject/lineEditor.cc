// lineEditor.cc
// CPSC 2620 Assignment 4
// Briana Smith
// March 8, 2017
//
// This class "LineEditor" uses a list and its operations
// to implement a one line text editor with a cursor.
// Functions include left and right to move the cursor, insert
// erase and apply to add, delete, and edit text. Ostream
// operator << outputs line of text and lower cursor.

#include "lineEditor.h"

//default constructor: intializes empty string with cursor on last character.
LineEditor::LineEditor()
{   cursor=text.end(); }

//functions:
//left
//This function moves the cursor to the left by one.
//If at the beginning of the list it does nothing.
void LineEditor::left()
{
   if(cursor!=text.begin())
      --cursor;
}

//right
//This function moves the cursor to the right by one.
//If at the end of the list it does nothing.
void LineEditor::right()
{
   if(cursor!=text.end())
      ++cursor;
}

//insert
//Inserts a character into the list at the cursor position.
//Cursor will be one after inserted string.
void LineEditor::insert(const string& s)
{
   int len = s.length();
   for(int i=0; i<len; i++)
      text.insert(cursor,s.at(i));
}

//erase
//Erases character at cursor.
//Cursor is positioned after erased character.
//If cursor is past end of line, does nothing.
void LineEditor::erase()
{
   if(cursor!=text.end())
      cursor=text.erase(cursor);
}

//change
//Replaces the character with c at cursor.
//Cursor is then positioned on changed character.
//If past end of line, change behaves as insert.
void LineEditor::change(char c)
{
   if(cursor!=text.end())
   {
      cursor=text.erase(cursor);
      text.insert(cursor,c);
      cursor--;
   }

   else
      text.insert(cursor,c);
}

//apply
//Every character c in the line has the f function applied.
//Replaces the character by f(c)
void LineEditor::apply(char(*f)(char c))
{
   list<char>::iterator it;
   for(it=text.begin(); it!=text.end(); ++it)
      *it=f(*it);
}

//operator <<
//ostream operator that allows output of LineEditor
ostream& operator<<(ostream& os, const LineEditor& le)
{
   list<char>::const_iterator it;
     
   for(it=le.text.begin(); it!=le.text.end(); ++it)
   {
      os<<*it;
   }
   os<<'$'<<endl;

   for(it=le.text.begin(); it!=le.text.end(); ++it)
   {
      if(it!=le.cursor)
	 os<<'-';
      else
	 os<<'^';
   }
   
   if(le.cursor==le.text.end())
      os<<'^';
   
   os<<endl;
   return os;
}
