# Web Crawler Project

## Description

Welcome to the Web Crawler project!

This repository contains two different versions of the web crawler:

1. **Iterative Code**: This version is the default execution and works better.

2. **Thread Pool**: The second version contains Thread Pool implementation. It's a work in progress and may not be perfect yet.
If you want to try it, pass True to using_threads argument (it's in execute_crawler method inside main.py)

## How to Run

To run the project, use the following command in the command line:

```
python main.py <start_url> <max_amount> <max_depth> <uniqueness>
```

Alternatively, you can use the following command with flags:

```
python main.py -url <start_url> -a <max_amount> -d <max_depth> -u <uniqueness>
```

Please replace <start_url>, <max_amount>, <max_depth>, and <uniqueness> with appropriate values for your use case.

## Data Saving
The scraped data will be saved in the "scraped_data" folder, as defined in the main.py file. If you prefer a different folder name, you can change it in the configuration file.

### Good Luck!
