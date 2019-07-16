/*
 * Polynomical implementation
 */

#ifndef _NCHAIN_SDK_POLYNOMIAL_H_
#define _NCHAIN_SDK_POLYNOMIAL_H_


#include <vector>
#include <string>
#include <iostream>
#include <BigNumbers/BigNumbers.h>


/// 
class Polynomial
{
  public:
 
    // construct empty
    Polynomial( ) = default ;


    // construct from BigNumber vector
    Polynomial( std::vector< BigNumber >& coefficients, int groupModulo = 0 ) ;

    // construct from String vector
    Polynomial( std::vector< std::string >& coefficients, int groupModulo = 0 ) ;

    /// Default destructor
    ~Polynomial() = default ;


    /**
    * Get the degree of the polynomial.
    * @return The degree (order) of the polynomial
    */
    int getDegree() { return m_coefficients.size() -1 ; }


    /**
    * Evaluate the polynomial at value x
    * @param x The value of x 
    * @return  The evaluated result 
    */
    BigNumber evaluate( const BigNumber& x ) 
    {
        BigNumber res ;
	    res.FromDec( std::to_string( 0 ) ) ;

        // Horners method for polynomial evaluation
        for( auto coef = m_coefficients.cbegin(); coef != m_coefficients.cend(); ++coef )
        {   
            res = ( res * x ) + *coef ;
        }

        return res;
    }    


    /*
     * Array access
     */
    BigNumber& operator [] (unsigned int index)                 { return m_coefficients[ index] ; }
    BigNumber const& operator [] (unsigned int index) const     { return m_coefficients[ index] ; }



  private:

    /* Push BigNumber to end of coefficients, using the modulo (if defined)
     */
    void push_back( BigNumber big ) ;

    /// coefficients array
    std::vector< BigNumber > m_coefficients ;    

   
    /// modulo 
    //<todo> do we want to store BigNumber not int ?
    int m_modulo ;


    friend std::ostream& operator<<( std::ostream &os, const Polynomial& p ) ; 
};




#endif 