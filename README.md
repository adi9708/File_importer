# Take Home Exercise
At Voltaiq, a big portion of our job is being able to create and develop importers for various types of customer data. In this exercise, you will be tasked with creating a basic importer that allows you to import data files in various formats.

1. Each file import should be able to be triggered with a single function call.
2. For as many of the test files complete the following.
   * Extract the metadata at the top of the data file. Write the metadata as key value pairs in a txt file to the results directory.
   * Import the data and write it as a csv in the results directory. Feel free to use any python packages to accomplish this task.
3. Plot all voltage traces across all files as a function of time in a single figure. Use any python-based plotter such as matplotlib, plotly, bokeh, etc.
4. Save the figure as a `.png` to the results folder.

**It is okay if you do not manage to get all the datafiles imported**, the focus of this exercise is the design of the importer. It may help to think about the importer in the context of configurability.

Some configuration options we recommend:
   * File path to read in
   * File path to output to
   * Normalization of units and column names

Use the differences in the data files to inspire more configuration options.

**Please do not spend more than four hours on this project.**

If you get stuck or have any questions, don't hesitate to reach out!

# Evaluation Guidelines
* Code clarity/readability
* Testing
* Requirements fulfilled
* Documentation
