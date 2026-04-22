# File Handling Project

This Python-based utility offers a flexible, memory-efficient solution for transforming flat-file datasets (CSV or TXT) into structured, type-cast dictionaries.

## User Guide
To use the parser, initialize the process by calling the convert function with your source filename. The utility will first present a live preview of the raw file content, prompting you to specify the number of header lines to skip. Following data cleaning, you can either manually define the key names and data types (int, float, bool, str) for each column or load a previously saved schema preset. The tool then iterates through the dataset, automatically casting each value to your specified type and appending the resulting dictionaries to your provided list for immediate use in your application logic.
