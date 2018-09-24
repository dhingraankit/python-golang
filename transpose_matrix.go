package main 

import (
	"fmt"
)

func main() {
	
	newMatrix := [3][3]int{}

    for m := 0; m <= 2; m++ {
		for n := 0; n <= 2; n++ {
			var j int
			fmt.Println("Enter an integer value : ")
   	 		_, err := fmt.Scanf("%d", &j)
   	 		newMatrix[m][n] = j
   	 		if err != nil {
        	fmt.Println(err)
   	 		}
   	 		continue
   		}
   		continue
	}
	fmt.Println("You formed the newMatrix: ", newMatrix)
	fmt.Println("So, here is the transpose of newMatrix:", transposeMyMatrix(newMatrix))
}



func transposeMyMatrix(newMatrix [3][3]int) [3][3]int {
	for m := 0; m <= 2; m++ {
		for n := m + 1; n <= 2; n++ { 
			newMatrix[m][n],newMatrix[n][m] = newMatrix[n][m], newMatrix[m][n]
			continue
		}
		continue
	}
	return newMatrix
}