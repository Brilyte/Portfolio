// lineEditor.h
// CPSC 2620 Assignment 4
// Briana Smith
// March 8, 2017
//
// This is the implementation file of the LineEditor class. It creates a list
// of characters and an iterator that acts as an editable line of text and
// a cursor.

#ifndef LINEEDITOR_H
#define LINEEDITOR_H

#include<list>
#include<string>
#include<iostream>

using namespace std;

class LineEditor{
  public:
   //default constructor
   LineEditor();   
   
   //Moves cursor right one char
   void right();
   //Moves cursor left one char
   void left();
   //Inserts string s at cursor
   void insert(const string& s);
   //Erases char at cursor
   void erase();
   //Changes at cursor to c
   void change(char c);
   //Applies function f to every char c, replaces char by f(c)
   void apply(char (*f)(char c));

   //Ostream operators works with cout to print LineEditor
   friend ostream& operator<<(ostream& os, const LineEditor& le);
   
   private:
   list<char> text;  //a list of char called text
   list<char>::iterator cursor; //a char list iterator called cursor

};

#endif
