# Milestone 4 Reflection

## Feedback Implementation

### Larger Feedback Items

1.  **Map Size and Clarity**:
    -   **Issue**: The map did not auto-fit to the right scale and it was a bit small with wide margins of white space. And U.S. border lines were unclear, making it hard to identify regions without zooming out.
    -   **Action Taken**: We moved the legend of the map to the top and removed the plotly toolbox to make room for bigger map. We also changed map into open-street map where state borders are more visible.
2.  **Data Consistency (Year Selection)**:
    -   **Issue**: The "Police Killing Victims by Month" plot included December 2015 data when only 2016 was selected.
    -   **Action Taken**: We fixed the data filtering logic to ensure the plot only displays data for the selected year.
3.  **Select All Button:**
    -   **Issue:** The buttons in the filters create unnecessary white spaces and are suggested to move next to the filter titles.

    -   **Action Taken**: Instead of adding "select all" button next to the filter title, we removed the buttons because the default is set to display all data already.

### Smaller Feedback Items

1.  **Scatter Map Aesthetics**:

    -   **Issue**: The colors in the scatter points are not consistent for each category.
    -   **Action Taken**: We fixed the color of the scatter points to be consistent for each category on the map.

2.  **Y-axis Title in the Distribution Bar Chart**:

    -   **Issue**: The y-axis title in the bar chart is repeatedly displayed along with the filter options.
    -   **Action Taken**: We removed y-axis title in the distribution bar chart.

3.  **State Labels and Legend**:

    -   **Issue**: State labels in the top n states bar chart and the legend in the time-series chart are unnecessary and obvious.
    -   **Action Taken**: We removed them.

4.  **Slider Width**:

    -   **Issue**: The slider is too wide, making the mouse movement span too large.
    -   **Action Taken**: We shortened the slider width.

5.  **Card Titles and Dropdown Bars**:

    -   **Issue**: Card titles and dropdown bars occupy two rows of space.
    -   **Action Taken**: We moved both dropdown bars next to the card titles.

6.  **Ordeing Age Group Categories**:

    -   **Issue**: Ordering of the age group categories is unnecessary in the source file.
    -   **Action Taken**: We ordered the categories in the cleaning step and export it to the processed data file directly to improve performance.

7.  **Cursor on the Top N States Bar Plot**:

    -   **Issue**: Although there are text instructions on the interactivity between the bar plot and the time-series plot, it might still not be intuitive enough for users to click on the bars.

    -   **Action Taken**: We changed the cursor to a pointer every time the user hovers over the bars.

8.  **Added Cache**:

    -   **Issue**: Performance might be slow when changing filters.

    -   **Action Taken**: Added caching to all functions that output charts by leveraging the `flask-caching` library.

9.  **Added favicon.ico**:

    -   Tiny touch-up on adding an icon for our dashboard.

------------------------------------------------------------------------

## Reflection on Dashboard Development

### Insights and Feedback

The feedback from Joel and peers was invaluable in refining our dashboard. Specifically, the suggestions to improve map scaling, ensure data consistency, and removing unnecessary components significantly enhanced the usability and clarity of our app.

### Support for Development

While the feedback was highly useful, we would have appreciated more guidance on further optimizing performance like parallelizng processes, as this was a challenge we encountered during implementation. Additionally, examples of advanced interactivity (e.g., linked brushing) would have been helpful for creating more dynamic visualizations.

### Known Issues

-   **Performance with Loading Map**: The dashboard may experience slight delays when loading the interactive scatter map, especially on slower devices.

### Strengths and Limitations

-   **Strengths**:
    -   Intuitive and user-friendly interface.
    -   Comprehensive visualizations (maps, bar charts and line charts).
    -   Effective use of interactivity to explore data.
-   **Limitations**:
    -   Limited to data from 2015-2016.
    -   Performance issues with loading map.
    -   Lack of advanced interactivity (e.g., linked brushing).
    -   Data is limited to exact counts of killings, which may not actually reflect the injustice against minority groups as we expected.

### Future Improvements

If we had more time, we would: - Expand the dataset to include more recent years. - Optimize further performance for large datasets. - Add advanced interactivity features (e.g., linked brushing, drill-down capabilities). - Incorporate additional demographic variables (e.g., socioeconomic status).

------------------------------------------------------------------------

## Conclusion

Overall, we are proud of the progress made on our dashboard and believe it effectively communicates critical insights about police killings in the U.S. The feedback from Joel and peers was instrumental in refining the app, and we look forward to continuing to improve it in the future.
