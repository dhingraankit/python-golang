package main

import (
	"fmt"
)

func main() {
	
	var arrayToBeSorted []int
	counter := 0
	for i := 0; counter < 5; i++ {
	var j int
    fmt.Println("Enter an integer value: ")
    _, err := fmt.Scanf("%d", &j)
	if err != nil {
        fmt.Println(err)
        continue
    }
    counter ++
    
    fmt.Println("You have entered : ", j)
    arrayToBeSorted = append(arrayToBeSorted,j)
	}
	fmt.Println("This is the array you entered: ",arrayToBeSorted)

	for j := 1; j < len(arrayToBeSorted); j++ {
		key := arrayToBeSorted[j]
		i := j - 1

		for i >= 0 && arrayToBeSorted[i] > key {
			arrayToBeSorted[i+1] = arrayToBeSorted[i]
			i = i - 1
		}

		arrayToBeSorted[i+1] = key
	}
	fmt.Println("I sorted it for you: ", arrayToBeSorted,". Thank me later! :)")
}