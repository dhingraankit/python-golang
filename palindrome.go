package main

import (
	"fmt"
	"strings"
)

func main() {
	var inputString string
	fmt.Println("Input a string here to test if it's a palindrome: ")
	fmt.Scanf("%s\n",&inputString)
	inputString = strings.ToLower(inputString)

	mid := len(inputString)/2
	last := len(inputString) - 1

	for i := 0; i <= mid; i++ {
		if inputString[i] != inputString[last - i] {
			fmt.Println("Not a Palindrome. Please try next time.")
			break
		}
	}
	fmt.Println("Yes!. It is a palindrome.")
}