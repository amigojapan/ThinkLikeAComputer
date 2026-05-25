for i in range(1, 4):
    output = ""
    
    # Inner loop controls the second number (1 through 3)
    for j in range(1, 4):
        # Append each equation to the row with spacing
        output += f"    {i} * {j} = {i * j}"
        
    # Print the completed row
    print(output)
    
    # Print a couple of blank lines to match your requested formatting
    print("\n")