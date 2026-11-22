import streamlit as st
import pandas as pd
import plotly.express as px



# # Load the dataset
file_path = r'Pakistan-educational-dataset.xlsx'
data = pd.read_excel(file_path)

# Centered Title
# st.markdown("<h1 style='text-align: center;'>Dashboard Edition 2024</h1>", unsafe_allow_html=True)

# Dashboard title
st.title('Pakistan Educational Dashboard')


# Sidebar for user selections
st.sidebar.header('User Selections')

# Add selection box for page navigation
page = st.sidebar.selectbox("Select Page", ["School Statistics", "Score Analysis"])

# Extract unique provinces and years
unique_provinces = data['Province'].unique()
unique_years = data['Year'].unique()

# Province selection
selected_provinces = st.sidebar.multiselect('Select Province(s)', unique_provinces)

# # Year selection
selected_years = st.sidebar.multiselect(
    'Select Year(s)', 
    unique_years.tolist(),  # Convert to list for multiselect
    default=[unique_years[0]]  # Pre-select the first year by default
)

# # Filter cities based on selected provinces
if selected_provinces:
    filtered_data = data[data['Province'].isin(selected_provinces)]
    unique_cities = filtered_data['City'].unique()

    # City selection
    selected_cities = st.sidebar.multiselect('Select City(ies)', unique_cities)

    if selected_cities:
        if page == "School Statistics":
            # Display selected cities and statistics for school counts
            st.write('You selected the following cities:')
            st.write(selected_cities)

            # Filter data for selected cities and years
            city_data = filtered_data[filtered_data['City'].isin(selected_cities) & (filtered_data['Year'].isin(selected_years))]

            # Display total primary, secondary, and overall schools using plots
            if not city_data.empty:
                # Prepare data for plotting
                school_counts = []
                for city in selected_cities:
                    city_specific_data = city_data[city_data['City'] == city]
                    total_primary_schools = city_specific_data['Number of primary schools'].sum()
                    total_secondary_schools = city_specific_data['Number of secondary schools'].sum()
                    total_schools = total_primary_schools + total_secondary_schools

                    # Append counts to the list for plotting
                    school_counts.append({'City': city, 'School Type': 'Total Schools', 'Count': total_schools})
                    school_counts.append({'City': city, 'School Type': 'Primary Schools', 'Count': total_primary_schools})
                    school_counts.append({'City': city, 'School Type': 'Secondary Schools', 'Count': total_secondary_schools})

                # Create a DataFrame for the plotting data
                school_counts_df = pd.DataFrame(school_counts)



                # Create a combined bar chart for school statistics
                fig = px.bar(
                    school_counts_df,
                    x='City',
                    y='Count',
                    color='School Type',
                    title=f'School Statistics in Selected Cities for {", ".join(map(str, selected_years))}',
                    labels={'Count': 'Number of Schools'},
                    height=400,
                    barmode='group'  # Group bars by city
                )

                # Update layout for better aesthetics
                fig.update_layout(
                    xaxis_title='City',
                    yaxis_title='Number of Schools',
                    title_font=dict(size=20, family='Arial, sans-serif'),
                    xaxis_title_font=dict(size=14),
                    yaxis_title_font=dict(size=14),
                    legend_title=dict(font=dict(size=14)),
                    hovermode='x unified'  # Show data on hover for all bars
                      
                )

                st.plotly_chart(fig)

                # Ensure the DataFrame is correct
                st.write(school_counts_df)  # Debugging line to check the DataFrame structure

                # --- Pie Chart for School Type Distribution ---
                pie_data = school_counts_df[school_counts_df['School Type'] != 'Total Schools']
                pie_fig = px.pie(
                    pie_data,
                    values='Count',
                    names='School Type',
                    title='Distribution of School Types',
                    height=400
                )
                st.plotly_chart(pie_fig)

                # Prepare data for additional plots
                additional_counts = []
                for city in selected_cities:
                    city_specific_data = city_data[city_data['City'] == city]
                    single_classroom = city_specific_data['Primary Schools with single classroom'].sum()
                    single_teacher = city_specific_data['Primary Schools with single teacher'].sum()
                    no_facility = city_specific_data['No Facility'].sum()
                    
                    # Append counts to the list for plotting
                    additional_counts.append({'City': city, 'Metric': 'Primary Schools with Single Classroom', 'Count': single_classroom})
                    additional_counts.append({'City': city, 'Metric': 'Primary Schools with Single Teacher', 'Count': single_teacher})
                    additional_counts.append({'City': city, 'Metric': 'No Facility', 'Count': no_facility})

                # Create a DataFrame for the additional plotting data
                additional_counts_df = pd.DataFrame(additional_counts)

                # Create a combined bar chart for additional metrics
                fig_additional = px.bar(
                    additional_counts_df,
                    x='City',
                    y='Count',
                    color='Metric',
                    title='Additional School Metrics in Selected Cities',
                    labels={'Count': 'Number of Schools'},
                    height=400,
                    barmode='group'  # Group bars by city
                )

                # Update layout for better aesthetics
                fig_additional.update_layout(
                    xaxis_title='City',
                    yaxis_title='Number of Schools',
                    title_font=dict(size=20, family='Arial, sans-serif'),
                    xaxis_title_font=dict(size=14),
                    yaxis_title_font=dict(size=14),
                    legend_title=dict(font=dict(size=14)),
                    hovermode='x unified'  # Show data on hover for all bars
                )

                st.plotly_chart(fig_additional)
            else:
                st.write('No data available for the selected city and year.')
            
            
        elif page == "Score Analysis":
            # Score Analysis page content
            st.title("Score Analysis")

            # Display selected cities
            st.write('You selected the following cities:')
            st.write(selected_cities)

            # Filter data for selected cities and years
            score_data = filtered_data[
            (filtered_data['City'].isin(selected_cities)) & 
            (filtered_data['Year'].isin(selected_years))
            ]

            if not score_data.empty:
        # Prepare data for plotting scores
                score_metrics = ['Education score', 'Enrolment score', 'Gender parity score', 'Learning score', 'School infrastructure score']
        
        # User selection for score metrics
                selected_metrics = st.multiselect(
                "Select score metrics to analyze:",
                options=score_metrics,
                 default=score_metrics  # Default to all available metrics
                )
        
                if not selected_metrics:
                    st.warning("Please select at least one score metric.")
                else:
            # Filter scores based on selected metrics
                    scores_df = score_data[['City', 'Year'] + selected_metrics]

            # User selection for plot type
                plot_type = st.radio("Select the type of plot to display:", ('Bar Plot', 'Line Plot'))

                if plot_type == 'Bar Plot':
                    melted_score_df = scores_df.melt(id_vars=['City', 'Year'], value_vars=selected_metrics, var_name='Score Type', value_name='Score Value')
                # Create a combined bar chart for scores
                    fig_scores = px.bar(
                        melted_score_df,
                        x='City',
                        y='Score Value',
                        color='Score Type',
                        title='Score Analysis for Selected Cities (Bar Plot)',
                        labels={'Score Value': 'Score', 'Score Type': 'Metric'},
                        height=400,
                        barmode='group'
                    )
                    st.plotly_chart(fig_scores)

                elif plot_type == 'Line Plot':
                # Create a line plot for scores with 'Year' included in x-axis
                    melted_scores_df = scores_df.melt(id_vars=['City', 'Year'], value_vars=selected_metrics, var_name='Score Type', value_name='Score Value')
                    fig_line = px.line(
                        melted_scores_df,
                        x='Year',
                        y='Score Value',
                        color='Score Type',
                        line_group='City',
                        line_shape='spline',
                        title='Score Analysis for Selected Cities (Line Plot)',
                        labels={'Score Value': 'Score', 'Score Type': 'Metric'},
                        height=400,
                        markers=True
                    )
                    st.plotly_chart(fig_line)

            # Display the scores data table
                st.subheader('Score Data Table')
                st.dataframe(scores_df)









                
        
        