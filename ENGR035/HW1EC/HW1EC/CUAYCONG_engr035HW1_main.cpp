#include "CUAYCONG_engr035HW1_Header.h"

int main()
{
	int op_choice;
	
	std::cout << "Welcome to 'vector calculator'!" << std::endl
		<< "Submitted by: Miguel Cuaycong" << std::endl
		<< "              ENGR035 Fall 2020" << std::endl << std::endl;

	std::cout << "Please choose the vector operation you wish to use:" << std::endl
		<< "(1)vector additon/subtraction" << std::endl
		<< "(2)angle between vectors" << std::endl
		<< "(3)vector dot product" << std::endl
		<< "(4)vector cross product" << std::endl;
	std::cin >> op_choice;

	if (op_choice == 1)
	{
		/*
		INSTRUCTIONS BEFORE RUNNING
		For adding/subtracting vectors, use the object below to input dimension and number of vectors.
		For example, two 3D vectors will be => vec v1(2,3)
		*/
		//---------
		vec v1(2, 3);
		//---------
		v1.addvec();
	}
	if (op_choice == 2)
	{
		//choice two instantiates vec object and calls the function within that calculates the angle between two vectors
		vec vec1;
		vec1.anglevec();
	}
	if (op_choice == 3)
	{
		//choice three instantiates vec object and calls the function within that calculates the dot product of two vectors
		vec vec1;
		vec1.dotvec();
	}
	if (op_choice == 4)
	{ 
		//choice four instantiates vec object and calls the function within that calculates the cross product of two vectors
		vec vec1;
		vec1.crossvec();
	}
}