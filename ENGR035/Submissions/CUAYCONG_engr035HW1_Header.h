#pragma once
#include <vector>
#include<iostream>
#include<string>
#include <math.h>   

class vec
{
	int nvectors; //stores the number of vectors
	int dvectors;
	double* vecptr;
	std::vector<std::vector<double>> vec_main;
public:
	vec();
	vec(int n, int d);
	void assign_vectors();
	void addvec();
	void anglevec();
	double anglevec(double** local_vec);
	void crossvec();
	void dotvec();
	

};

vec::vec()
	:nvectors(0), dvectors(0)
{

}
vec::vec(int n, int d)
	: nvectors(n), dvectors(d)
{
	std::cout << "Vector addition/subtraction operation chosen."<< std::endl<<"Make sure to check the instructions in the comments under int main()" << 
		std::endl << std::endl;
	std::vector<std::vector<double>> local_vec_main(nvectors, std::vector<double>(dvectors, 0));
	vec::vec_main = local_vec_main;
	assign_vectors();


}

void vec::assign_vectors()
{
	for (int i = 0; i < nvectors; i++)
	{
		for (int j = 0; j < dvectors; j++)
		{
			std::cout << "Please enter values for the " << j+1 << " dimension of vector " << i+1 << ":" << std::endl;
			std::cin >> vec_main[i][j];
		}
	std::cout << "vector " << i + 1 << ": < ";
		for (int j = 0; j < dvectors; j++)
		{
			std::cout << vec_main[i][j]  << " " ;
		}
	std::cout << " >" << std::endl;
	}

}
void vec::addvec()
{
	double* addendvector;
	addendvector = new double[nvectors];
	double* res_vec;
	res_vec = new double[dvectors];
	std::vector<std::vector<double>> local_vec_main(nvectors, std::vector<double>(dvectors, 0));
	local_vec_main = vec_main;

	std::cout << "When prompted, if you wish to add vector 1 and 2 given five vectors, simply input \n1\n1\n0\n0\n0" << std::endl
		<< "If you wish to add half of vector 1 and twice of vector 2, simply input \n0.5\n2\n0\n0\n0" << std::endl;

	for (int i = 0; i < nvectors; i++)
	{
		std::cout << "Please enter the scalar of vector " << i + 1  << std::endl;
		std::cin >> *(addendvector + i);
	}
	for (int i = 0; i < nvectors; i++)
	{
		for (int j = 0; j < dvectors; j++)
		{
			local_vec_main[i][j] = addendvector[i] * vec_main[i][j];
		}
	}
	std::cout << "The resultant vector is: < ";
	for (int i = 1; i < nvectors; i++)
	{
		for (int j = 0; j < dvectors; j++)
		{
			res_vec[j] = local_vec_main[0][j] + local_vec_main[i][j];
			std::cout  << res_vec[j] << " ";
		}
	}
	std::cout << ">" << std::endl;


}

void vec::anglevec()
{
	int local_dvectors;
	int dotproduct = 0;
	double result = 0;
	double sum = 0;
	

	std::cout << "Enter the dimension of vectors: " << std::endl;
	std::cin >> local_dvectors;
	double** local_vec_main = new double* [local_dvectors];
	double* magnitude = new double [local_dvectors];

	for (int i = 0; i < local_dvectors; ++i)
	{
		local_vec_main[i] = new double[2];
	}



	for (int i = 0; i < 2; i++)
	{
		for (int j = 0; j < local_dvectors; j++)
		{
			std::cout << "Please enter values for the " << j + 1 << " dimension of vector " << i + 1 << ":" << std::endl;
			std::cin >> local_vec_main[i][j];
		}

	std::cout << "vector " << i + 1 << ": < ";
	for (int j = 0; j < dvectors; j++)
	{
		std::cout << local_vec_main[i][j] << " ";
	}
	std::cout << " >" << std::endl;
	}
	for (int i = 0; i < local_dvectors; i++)
	{
		dotproduct = local_vec_main[0][i] * local_vec_main[1][i] + dotproduct;

	}
	for (int j = 0; j < 2; j++)
	{
		for (int i = 0; i < local_dvectors; i++)
		{
			sum = pow(2,local_vec_main[j][i]) + sum;
		}
		magnitude[j] = pow(1 / 2, sum);
	}
	result = acos(dotproduct / (magnitude[0] * magnitude[1]));
	std::cout << "the angle between is: " << result <<"radians" <<std::endl;
	
}
double vec::anglevec(double** local_vec_main)
{
	int local_dvectors = 2;
	int dotproduct = 0;
	double sum = 0;


	double* magnitude = new double[local_dvectors];




	for (int i = 0; i < local_dvectors; i++)
	{
		dotproduct = local_vec_main[0][i] * local_vec_main[1][i] + dotproduct;

	}
	for (int j = 0; j < 2; j++)
	{
		for (int i = 0; i < local_dvectors; i++)
		{
			sum = pow(2, local_vec_main[j][i]) + sum;
		}
		magnitude[j] = pow(1 / 2, sum);
	}
	return acos(dotproduct / (magnitude[0] * magnitude[1]));
}
void vec::crossvec()
{
	int local_dvectors;
	double result = 0;
	double sum = 0;

	std::cout << "Enter the dimension of vectors: " << std::endl;
	std::cin >> local_dvectors;
	double** local_vec_main = new double* [local_dvectors];
	double* magnitude = new double[local_dvectors];


	for (int i = 0; i < local_dvectors; ++i)
	{
		local_vec_main[i] = new double[2];
	}


	for (int i = 0; i < 2; i++)
	{
		for (int j = 0; j < local_dvectors; j++)
		{
			std::cout << "Please enter values for the " << j + 1 << " dimension of vector " << i + 1 << ":" << std::endl;
			std::cin >> local_vec_main[i][j];
		}

		std::cout << "vector " << i + 1 << ": < ";
		for (int j = 0; j < dvectors; j++)
		{
			std::cout << local_vec_main[i][j] << " ";
		}
		std::cout << " >" << std::endl;
	}
	for (int j = 0; j < 2; j++)
	{
		for (int i = 0; i < local_dvectors; i++)
		{
			sum = pow(2, local_vec_main[j][i]) + sum;
		}
		magnitude[j] = pow(1 / 2, sum);
	}
	double angle = anglevec(local_vec_main);
	result = angle * (magnitude[0] * magnitude[1]);
	std::cout << "The cross product is "<< result << " perpendicular to the two vectors" ;
	
}
void vec::dotvec()
{
	
	int local_dvectors;
	int result = 0;

	std::cout << "Enter the dimension of vectors: " << std::endl;
	std::cin >> local_dvectors;
	double** local_vec_main = new double* [local_dvectors];


	for (int i = 0; i < local_dvectors; ++i)
	{
		local_vec_main[i] = new double[2];
	}


	for (int i = 0; i < 2; i++)
	{
		for (int j = 0; j < local_dvectors; j++)
		{
			std::cout << "Please enter values for the " << j + 1 << " dimension of vector " << i + 1 << ":" << std::endl;
			std::cin >> local_vec_main[i][j];
		}

		std::cout << "vector " << i + 1 << ": < ";
		for (int j = 0; j < dvectors; j++)
		{
			std::cout << local_vec_main[i][j] << " ";
		}
		std::cout << " >" << std::endl;
	}

	for (int i = 0; i < local_dvectors; i++)
	{
		result = local_vec_main[0][i] * local_vec_main[1][i] + result;

	}
	std::cout << "The dot product is " << result << std::endl;


}
