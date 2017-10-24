// list.h
// Briana Smith
// CPSC 2620 Assignment 5
//
// Header file for list class. Doubly linked list class with dummy header,
// iterator and element members.

#ifndef LIST_H
#define LIST_H

using namespace std;

class List
{
  private:
   
   class Element
   {
     public:
     Element(char item='\0', Element* n1=nullptr, Element* n2=nullptr)
	 : data(item), nextPtr(n1), prevPtr(n2){}
      char data;
      Element *nextPtr;
      Element *prevPtr;
   };

  public:
   class Iterator
   {
      friend class List; //so List has access to currPtr below

     public:
      Iterator(Element *e = nullptr) : currPtr(e) {}
      bool operator==(const Iterator&) const; //equality overload
      bool operator!=(const Iterator&) const; //inequality overload
      const char& operator*() const; //dereference operator(r-value ver)
      char& operator*(); //dereference operator (l-value ver)
      Iterator& operator++(); //pre-increment
      Iterator& operator--(); //post-increment
      
     private:
      Element* currPtr;
   };

   friend class Iterator; //so Iterator class can access private data below

   //List class members:
   List(); //default constructor
   ~List(); //destructor
   
   void insert(Iterator, char); //inserts before current iterator position
   void erase(Iterator); //erase element at current iterator position
   Iterator begin() const; //iterator to first element in list
   Iterator end() const; //iterator to end of list ie.headPtr(dummy header)
                         //else won't print last element
   void push_front(char); //add Element to front of list
   void push_back(char); //add Element to end of list
   
  private:
   Element* headPtr;
  
};

#endif
