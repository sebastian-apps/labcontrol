from tkinter import filedialog



def saveas(ctx):
    """ Save the data """
    # there's still a permission error for overwriting files if the csv file is open in excel.
    directory = filedialog.asksaveasfilename(defaultextension="csv", filetypes=[("CSV file", ".csv")])
    # directory is directory + filename.csv
    if directory is not None and directory != "": # None indicates cancelled by user
        saveCSV(ctx, directory)



def save(ctx):
    """ Save the data """
    if ctx.filesaved == "":  # If data had not previously been saved, go to saveas.
        ctx.saveas()
    else:
        saveCSV(ctx, ctx.filesaved)



def saveCSV(ctx, directory):
    """ Save the data as CSV """
    try:
        file  = open(directory, "w")
        # write header row
        param_order = ctx.config.get("export_order").copy()
        headers = [ctx.config.get("params").get(param).get("name") for param in param_order]
        headers.insert(0, "Time (s)")
        datastring = ", ".join(headers)
        # write to CSV
        file.write(f"{datastring}\n")  

        # FORMAT DATA, READY FOR PRINTING TO CSV
        # Need to write out data row by row, all keys simultaneously.
        # Create 2D array (list of lists): each column (left to right) is dictacted by config.get("export_order")
        param_order.insert(0, "time")
        num_rows = len(ctx.plotdata.get("time")) # time was selected arbitrarily to get num_rows.
        table = [[str(ctx.plotdata.get(param)[i]) for param in param_order] for i in range(num_rows)]

        # Remove all 'nan' strings, replace with empty with arbitrary string value
        table = [["-" if val == "nan" else val for val in row] for row in table]
        # Remove rows with duplicate time values. Keep the most recent of the duplicates.
        table2 = []
        prev_time_value = None
        for row in table:
            if row[0] == prev_time_value:
                table2.pop() # If row has same time value as previous row, then pop the previous.
            table2.append(row)
            prev_time_value = row[0]

        # write to CSV
        for row in table2:
            datastring = ", ".join(row)
            file.write(f"{datastring}\n")  
        file.close()
        print(f"File {directory} saved.")
        ctx.filesaved = directory
        ctx.show_message("File saved.")


    except PermissionError:
        ctx.show_message("Error in saving!\nFile is open.\nPlease close file before saving.")
    except Exception as e:
        ctx.show_message("Error in saving!")