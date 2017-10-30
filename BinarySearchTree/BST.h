// BST.h
// Briana Smith
// April 4, 2017
// Assignment 6 - Question 1
// This is a binary search tree class (BST class). Each Node stores a string
// and vector<string>, and has two pointers (lPtr and rPtr) to next nodes.
// Can emulate map with string key, vector<string> value pairs, and included
// functions.

#ifndef BST_H
#define BST_H

#include<string>
#include<vector>
using namespace std;

class BST
{

  public:
   
   BST(); //Constructor
   ~BST(); //Destructor
   
   // Overloaded Subscript Operator
   // Implemented the same way as map associative container.
   // If the key does not exist a new node is inserted into the BST in
   // the proper location. If the key does exist a string is added to the
   // "value" vector.
   vector<string>& operator[](const string&);

   // function for user to traverse the BST
    void traverse(void(*f)(const string&, vector<string>&));

  private:
   // BSTs consist of nodes
   struct Node
   {
      Node(string s = "", Node* l=nullptr, Node* r=nullptr)
      :key{s},lPtr{l},rPtr{r} {}
      string key;
      vector<string> value;
      Node* lPtr;
      Node* rPtr;
   };

   // pointer to Node
   Node* root;

   // destroys Nodes, used to deconstruct tree
   void destroy(Node*&);
  
   // function to find Node in the BST, if not found nullptr returned
   Node* find(Node*, const string&);

   // function to insert a node if key and str don't match, returns node pointer
   Node* insert(Node*&, const string&);

   // private traverse, takes function to traverse tree
   void traverse(Node*,void (*f)(const string&, vector<string>&));
 
};

#endif
