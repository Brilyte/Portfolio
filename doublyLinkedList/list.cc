// list.cc
// Briana Smith
// CPSC 2620 Assignment 5

// This file imitates a doubly linked list class with a dummy header.
// Includes list members: constructor, push back, push front, insert, begin,
// end, and iterator members.

#include "list.h"

//*****************************************************************************
// List Members
//*****************************************************************************

//default constructor
List::List()
{
   headPtr = new Element(); //dummy node
   headPtr->nextPtr = headPtr;
   headPtr->prevPtr = headPtr;
}

//deconstructor
List::~List()
{
   while(headPtr->nextPtr!=headPtr)
   {
      Element* tempPtr = headPtr->nextPtr;
      tempPtr->nextPtr->prevPtr = headPtr;
      headPtr->nextPtr = tempPtr->nextPtr;
      delete tempPtr;
   }

   delete headPtr;
}

//push_back
//adds char c to end of list
void List::push_back(char c)
{
   Element* tempPtr = new Element(c, headPtr, headPtr->prevPtr);
   headPtr->prevPtr->nextPtr=tempPtr;
   headPtr->prevPtr=tempPtr;
}

//push_front
//adds char c to begin of list
void List::push_front(char c)
{
   Element* tempPtr = new Element(c, headPtr->nextPtr, headPtr);
   headPtr->nextPtr->prevPtr = tempPtr;
   headPtr->nextPtr = tempPtr;
}

//begin
//moves iterator to begin
List::Iterator List::begin() const
{
   return Iterator(headPtr->nextPtr);
}

//end
//moves iterator one past the end
List::Iterator List::end() const
{
   return Iterator(headPtr);
}

//insert
//inserts char at iterator
void List::insert(Iterator it, char c)
{
      Element* tempPtr = new Element(c, it.currPtr, it.currPtr->prevPtr);
      it.currPtr->prevPtr->nextPtr = tempPtr;
      it.currPtr->prevPtr = tempPtr;  
}

//erase
//erases char at it
void List::erase(Iterator it)
{
   if(it!=end())
   {
      it.currPtr->prevPtr->nextPtr = it.currPtr->nextPtr;
      it.currPtr->nextPtr->prevPtr = it.currPtr->prevPtr;
      delete it.currPtr;
   }
}

//*****************************************************************************
// Iterator Members
//*****************************************************************************

// == operator
// checks equality of iterators
bool List::Iterator::operator==(const Iterator& it) const
{
   return this->currPtr==it.currPtr;
}

// != operator
// checks inequality of iterators
bool List::Iterator::operator!=(const Iterator& it) const
{
   return this->currPtr!=it.currPtr;
}

// Dereference operator *
// r-value version
// Returns data of element iterator is pointing to
const char& List::Iterator::operator*() const
{
   return currPtr->data;
}

// Dereference operator *
// l-value version
// Replaces data of element iterator is pointing to
char& List::Iterator::operator*()
{
   return currPtr->data;
}

// Pre-increment operator ++
// Increments the iterator by one
List::Iterator& List::Iterator::operator++()
{
   currPtr = currPtr->nextPtr;
   return *this;
}

// Pre-decrement operator --
// Decrements the iterator by one
List::Iterator& List::Iterator::operator--()
{
   currPtr = currPtr->prevPtr;
   return *this;
}

