import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

# Load CSV file from Datasets folder
df1 = pd.read_csv('moviesData.csv')

#create list of separate genres
genres = df1['Genres'].unique()
genreList = ["All"]
for genre in genres:
    try:
        sep_genre = genre.split(',')
    except:
        pass
    for singleGenre in sep_genre:
        if singleGenre not in genreList:
            genreList.append(singleGenre)

#create list of separate language
languages = df1['Language'].unique()
langList = ["All"]
for language in languages:
    try:
        sep_language = language.split(',')
    except:
        pass
    for singleLanguage in sep_language:
        if singleLanguage not in langList:
            langList.append(singleLanguage)

#create list of separate age groups
ages = df1['Age'].unique()
ageList = ["All"]
for age in set(ages)-(set(["all"])):
    if age not in ageList and not pd.isna(age):
        #age = age.replace("+", "")
        ageList.append(age)
ageList[1:].sort()

#initialize global variables to be used among all pages
global globalGenre
globalGenre = ["All"]

global globalRatingBool
globalRatingBool = None
global globalRating
globalRating = None

global globalLengthBool
globalLengthBool = None
global globalLengths
globalLengths = None

global globalYearBool
yearRangeBool = None
global globalYears
globalYears = None

global globalLanguage
globalLanguage = ["All"]

global globalAgeGroup
globalAgeGroup = ["All"]



app = dash.Dash(__name__)


# initializing layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#home page layout
home_page = html.Div(children=[
    html.H1(className = 'center',children='PerfectMovie',
        style={
            'textAlign': 'center',
            'color': '#ef3e18'
        }
    ),
    html.Div(children=[
        dcc.Link(
            html.Button(children=[
                html.Img(
                    src=app.get_asset_url('go.png'),
                    style={'width':'30%'}
                ),
                html.Div("Press Go to start",
                         style={'font-family': 'Courier New', 'font-weight': 'bold', 'font-size':'15px', 'color': '#00284d'})],
                style={'background': 'transparent', 'border':'0'}
            ),
            href='/mainPage')
    ], style= {'textAlign': 'center'}),
    html.Div(className='row', children=[
        html.Div(className= 'column', children=[
            html.Div(children=[html.Div(className= 'listHeader', children="About: "),
                               html.Ul(children=[
                                   html.Li(children= "This web application utilizes a "
                                                                            "Kaggle database based on movie "
                                                                            "records from the four most popular streaming services"),
                                   html.Li(className='listIndent0',
                                           children= "Netflix, Hulu, Prime Video, Disney+")
                               ])],
                     style={'margin-top':'15%', 'font-family': 'Courier New'}
             ),
            html.Div(children=[html.Div(className= 'listHeader', children="The Goal: "),
                               html.Ul(children=[
                                   html.Li(className='nextItem',
                                           children='The goal of this web application is to provide you, the user, with important '
                                                    'information regarding the types of movies on popular streaming services and '
                                                    'help you make a more informed decision on which streaming service may be best for you')
                               ])],
                     style={'margin-top': '8%', 'font-family': 'Courier New'}
            )
        ]),
        html.Div(className= 'column', children=[
            html.Div(children=[html.Div(className='listHeader', children="The Elements: "),
                               html.Ul(children=[
                                   html.Li(children= "The elements of the graph page can effectively be broken into three categories"),
                                   html.Li(className='listIndent0',
                                           children= html.P(children=["The ", html.Span(className='listHeader', children="Bar Graph"),
                                                                      " is used to display the amount of movies on "
                                                                      "each streaming service corresponding to the filter setting which are set. "
                                                                      "This element is found in the middle of the screen"])
                                           ),
                                   html.Li(className='listIndent0',
                                           children=html.P(
                                               children=["The ", html.Span(className='listHeader', children="6 Filters"),
                                                         " are used to manipulate which data will be found in the bar graph. "
                                                         "Each filter corresponds to a different data value associated with each movie."
                                                         "Three filters are in the form of dropdowns and can be found above the bar graph. "
                                                         "The other three filters are in the form of sliders and can be found under the bar graph"])
                                           ),
                                   html.Li(className='listIndent0',
                                           children=html.P(
                                               children=["The ", html.Span(className='listHeader', children="Toggle Checkboxes"),
                                                         " are used to turn specific sliders on and off as well as toggle the percentage view of the bar graph. "
                                                         "The toggle checkboxes found under each slider filter can be used to turn the corresponding filter on or off."
                                                         "The 'Show Percentage View' toggle checkbox can be used to show the bar graoh as a percentage, "
                                                         "meaning each bar in the bar graph shows the percentage of movies matching the filter "
                                                         "criteria with respect to the total number of movies on ech streaming service. "
                                                         "When a Toggle Checkbox is checked, it means the value is set to 'on'"])
                                           )

                               ])],
                     style={'margin-top': '15%', 'font-family': 'Courier New'}
            )
        ])

    ]),
    html.Img(
        src=app.get_asset_url('streaming.png'),
        style={'display': 'block', 'margin-left': 'auto', 'margin-top': '5%','margin-right': 'auto' , 'width':'75%'}
    )


], style={'background-color': '#D3D3D3', 'position':'relative', 'width':'100%', 'height':'100%'})


#main page layout
page_1_layout = html.Div(children=[
    html.H1(children='PerfectMovie',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Streaming Service records', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    dcc.Link(
        html.Button(children=[
            html.Img(
                src=app.get_asset_url('back.png'),
                style={'width': '30%'}
            ),
            html.Div("Back to home",
                     style={'font-weight': 'bold', 'font-size': '12px', 'textAlign': 'center', 'color': '#00284d'})],
            style={'background': 'transparent', 'border': '0', 'left': '5%'}
        ),
        href='/'
    ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Filter Categories', style={'color': '#00284d'}),
    html.Div(children = [

        # create genre dropdown
        html.Div(children = [
            dcc.Dropdown(
                id='select-Genre',
                options=[
                    {'label': genre, 'value': genre} for genre in genreList
                ],
                multi = True,
                placeholder='Select Genre...',
                clearable = False,
                searchable = True,
                style = {"background": "#e6f3ff", 'color': '#00284d'}
            )
        ], style= {'width': '33%'}),

        # create language dropdown
        html.Div(children=[
            dcc.Dropdown(
                id='select-Language',
                options=[
                    {'label': language, 'value': language} for language in langList
                ],
                multi = True,
                placeholder='Select Language...',
                clearable=False,
                searchable=True,
                style = {"background": "#e6f3ff", 'color': '#00284d'}
            )
        ], style={'width': '33%'}),

        # create age dropdown
        html.Div(children=[
            dcc.Dropdown(
                id='select-Age-Group',
                options=[
                    {'label': age, 'value': age} for age in ageList
                ],
                multi= True,
                placeholder='Select Age Group...',
                clearable=False,
                searchable=True,
                style={"background": "#e6f3ff", 'color': '#00284d'}
            )
        ], style={'width': '33%'}),

	], style={'display': 'flex'}),
    html.Div(children= [
        dcc.Graph(id='graph1'),
            html.Div(children=[
                html.Div(className = 'four columns', children = [
                    dcc.Link(
                        html.Button('Show movie List', style={'width':'100%'}),
                        href='/netList',
                        style = {"position":"absolute", "left":"12.5%", 'width':'7%'}),
                    dcc.Link(
                        html.Button('Show movie List', style={'width':'100%'}),
                        href='/huList',
                        style = {"position":"absolute", "left":"35.3%", 'width':'7%'}),
                    dcc.Link(
                        html.Button('Show movie List', style={'width':'100%'}),
                        href='/pvList',
                        style = {"position":"absolute", "left":"58.1%", 'width':'7%'}),
                    dcc.Link(
                        html.Button('Show movie List', style={'width':'100%'}),
                        href='/disList',
                        style = {"position":"absolute", "left":"80.5%", 'width':'7%'})
                    ], style = {"position": "relative", "top": "-60px"})

    ])
    ], style={'textAlign':'center', 'width': '100%'}),


    #create percentage toggle
    html.Div(className='toggleRow', children=[
        dcc.Checklist(
            id="percentToggle",
            options=[
            {'label': 'Show Percentage View', 'value': 'Percentage'}
            ],
            style={'color': '#00284d'}
        )
    ]),

    #create filters
    html.Div(children = [

        #create minimum rating slider
        html.Div(children = [
            html.Div('Select Minimum Rotten Tomatoes Rating',
                     style={'textAlign': 'center',
                            'color': '#00284d',
                            'font-size': 'medium',
                            'margin-bottom': '6px'}),
            dcc.Slider(
                id='select-Rating',
                min=0,
                max=100,
                step=1,
                value=0,
                marks={
                    0: {'label': '0%', 'style': {'color': '#77b0b1'}},
                    25: {'label': '25%', 'style': {'color': '#77b0b1'}},
                    50: {'label': '50%', 'style': {'color': '#77b0b1'}},
                    75: {'label': '75%', 'style': {'color': '#77b0b1'}},
                    100: {'label': '100%', 'style': {'color': '#77b0b1'}}
                },
                included = True
            ),
            html.Div(id='rating-output', style={'textAlign': 'center',
                                                'color': '#00284d',
                                                'font-size': 'medium',
                                                'margin-bottom': '6px'}),

            #create toggle for rating filter
            dcc.Checklist(
                id="ratingToggle",
                options=[
                    {'label': 'Apply Rating Filter', 'value': 'ratingSwitch'}
                ],
                value=[],
                style={'textAlign': 'center', 'color': '#00284d', 'font-weight':'bold'}
            )
        ], style={'width': '33%', 'margin-top': '6px'}),

        #create runtime range slider
        html.Div(children = [
            html.Div('Select Length Range',
                     style={'textAlign': 'center',
                            'color': '#00284d',
                            'font-size': 'medium',
                            'margin-bottom': '6px'}),
            dcc.RangeSlider(
                id='select-Length',
                min=1,
                max=1256,
                step=1,
                value=[1, 1256],
                marks={
                    1: {'label': '1 min', 'style': {'color': '#77b0b1'}},
                    314: {'label': '314 mins', 'style': {'color': '#77b0b1'}},
                    628: {'label': '628 mins', 'style': {'color': '#77b0b1'}},
                    948: {'label': '948 mins', 'style': {'color': '#77b0b1'}},
                    1256: {'label': '1256 mins', 'style': {'color': '#77b0b1'}}
                },
                included=True,
                allowCross=False
            ),
            html.Div(id='length-output', style={'textAlign': 'center',
                                                'color': '#00284d',
                                                'font-size': 'medium',
                                                'margin-bottom': '6px'}),
            #create toggle for runtime range filter
            dcc.Checklist(
                id="lengthToggle",
                options=[
                    {'label': 'Apply Length Filter', 'value': 'lengthSwitch'}
                ],
                value=[],
                style={'textAlign': 'center', 'color': '#00284d', 'font-weight':'bold'}
            )
        ], style= {'width': '33%', 'margin-top': '6px'}),

        #create year range slider
        html.Div(children = [
            html.Div('Select Year Range',
                     style={'textAlign': 'center',
                            'color': '#00284d',
                            'font-size': 'medium',
                            'margin-bottom': '6px'}),
            dcc.RangeSlider(
                id='select-Age',
                min = 1902,
                max = 2020,
                step = 1,
                value = [1902, 2020],
                marks = {
                    1902: {'label': 1902, 'style': {'color': '#77b0b1'}},
                    1931: {'label': 1931, 'style': {'color': '#77b0b1'}},
                    1961: {'label': 1961, 'style': {'color': '#77b0b1'}},
                    1990: {'label': 1990, 'style': {'color': '#77b0b1'}},
                    2020: {'label': 2020, 'style': {'color': '#77b0b1'}}
                },
                included = True,
                allowCross = False
            ),
            html.Div(id='year-output', style={'textAlign': 'center',
                                                'color': '#00284d',
                                                'font-size': 'medium',
                                                'margin-bottom': '6px'}),

            #create toggle for Year range filter
            dcc.Checklist(
                id="ageToggle",
                options=[
                    {'label': 'Apply Year Filter', 'value': 'yearSwitch'}
                ],
                value=[],
                style={'textAlign': 'center', 'color': '#00284d', 'font-weight':'bold'}
            )
        ], style={'width': '33%', 'margin-top': '6px'})
    ], style={'display': 'flex'})
])

#create layout for list of netflix movies
netflixBarList = html.Div(children=[
    html.H1(children='PerfectMovie',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Streaming Service records', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    dcc.Link(
        html.Button(children=[
            html.Img(
                src=app.get_asset_url('back.png'),
                style={'width': '30%'}
            ),
            html.Div("Back to graph",
                     style={'font-weight': 'bold', 'font-size': '12px', 'textAlign': 'center', 'color': '#00284d'})],
            style={'background': 'transparent', 'border': '0', 'left': '5%'}
        ),
        href='/mainPage'
    ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Netflix Barchart movie list with matching search criteria', style={'color': '#df1e56'}),
    html.Div('This List represents all movies given your search criteria on netflix'),
    html.Br(),
    html.Br(),
    dcc.Checklist(
        id="listGen",
        options=[
            {'label': 'Create List', 'value': 'createList'}
        ],
        value=['createList'],
        style={'textAlign': 'center'}
    ),
    dt.DataTable(id='netflixTable',
                 columns=[{'name': movie, 'id': movie} for movie in (set(df1.columns) - set(["Netflix","Hulu", "Prime Video", "Disney+"]))],
                 style_cell={'textAlign': 'left'})

])

#create layout for list of hulu movies
huluBarList = html.Div(children=[
    html.H1(children='PerfectMovie',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Streaming Service records', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    dcc.Link(
        html.Button(children=[
            html.Img(
                src=app.get_asset_url('back.png'),
                style={'width': '30%'}
            ),
            html.Div("Back to graph",
                     style={'font-weight': 'bold', 'font-size': '12px', 'textAlign': 'center', 'color': '#00284d'})],
            style={'background': 'transparent', 'border': '0', 'left': '5%'}
        ),
        href='/mainPage'
    ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Hulu Barchart movie list with matching search criteria', style={'color': '#df1e56'}),
    html.Div('This searchable List represents all movies given your search criteria on netflix'),
    html.Br(),
    html.Br(),
    dcc.Checklist(
        id="listGen",
        options=[
            {'label': 'Create List', 'value': 'createList'}
        ],
        value=['createList'],
        style={'textAlign': 'center'}
    ),
    dt.DataTable(id='huluTable',
                 columns=[{'name': movie, 'id': movie} for movie in (set(df1.columns) - set(["Netflix","Hulu", "Prime Video", "Disney+"]))],
                 style_cell={'textAlign': 'left'})

])

#create layout for list of prime video movies
primeBarList = html.Div(children=[
    html.H1(children='PerfectMovie',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Streaming Service records', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    dcc.Link(
        html.Button(children=[
            html.Img(
                src=app.get_asset_url('back.png'),
                style={'width': '30%'}
            ),
            html.Div("Back to home",
                     style={'font-weight': 'bold', 'font-size': '12px', 'textAlign': 'center', 'color': '#00284d'})],
            style={'background': 'transparent', 'border': '0', 'left': '5%'}
        ),
        href='/mainPage'
    ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Prime Video Barchart movie list with matching search criteria', style={'color': '#df1e56'}),
    html.Div('This searchable List represents all movies given your search criteria on netflix'),
    html.Br(),
    html.Br(),
    dcc.Checklist(
        id="listGen",
        options=[
            {'label': 'Create List', 'value': 'createList'}
        ],
        value=['createList'],
        style={'textAlign': 'center'}
    ),
    dt.DataTable(id='primeTable',
                 columns=[{'name': movie, 'id': movie} for movie in (set(df1.columns) - set(["Netflix","Hulu", "Prime Video", "Disney+"]))],
                 style_cell={'textAlign': 'left'})

])

#create layout for list of Disney+ movies
disneyBarList = html.Div(children=[
    html.H1(children='PerfectMovie',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Streaming Service records', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    dcc.Link(
        html.Button(children=[
            html.Img(
                src=app.get_asset_url('back.png'),
                style={'width': '30%'}
            ),
            html.Div("Back to home",
                     style={'font-weight': 'bold', 'font-size': '12px', 'textAlign': 'center', 'color': '#00284d'})],
            style={'background': 'transparent', 'border': '0', 'left': '5%'}
        ),
        href='/mainPage'
    ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Disney Barchart movie list with matching search criteria', style={'color': '#df1e56'}),
    html.Div('This searchable List represents all movies given your search criteria on netflix'),
    html.Br(),
    html.Br(),
    dcc.Checklist(
        id="listGen",
        options=[
            {'label': 'Create List', 'value': 'createList'}
        ],
        value=['createList'],
        style={'textAlign': 'center'}
    ),
    dt.DataTable(id='disneyTable',
                 columns=[{'name': movie, 'id': movie} for movie in (set(df1.columns) - set(["Netflix","Hulu", "Prime Video", "Disney+"]))],
                 style_cell={'textAlign': 'left'})

])

#callback to dynamically update string value under rating filter
@app.callback(Output('rating-output', 'children'),
              [Input('select-Rating', 'drag_value')])
def display_value(drag_value):
    return 'More than {}%'.format(drag_value)

#callback to dynamically update string value under runtime range filter
@app.callback(Output('length-output', 'children'),
              [Input('select-Length', 'drag_value')])
def display_value(drag_value):
    if drag_value is None:
        return 'Between {} and {} mins'.format(0, 0)
    return 'Between {} and {} mins'.format(drag_value[0], drag_value[1])

#callback to dynamically update string value under Year range filter
@app.callback(Output('year-output', 'children'),
              [Input('select-Age', 'drag_value')])
def display_value(drag_value):
    if drag_value is None:
        return 'Between {} and {} mins'.format(0, 0)
    return 'Created between {} and {}'.format(drag_value[0], drag_value[1])

#callback to create the barchart
@app.callback(Output('graph1', 'figure'),
              [Input('percentToggle', 'value'),
               Input('select-Genre', 'value'),
               Input('select-Age', 'drag_value'),
               Input('select-Length', 'drag_value'),
               Input('select-Rating', 'drag_value'),
               Input('ratingToggle', 'value'),
               Input('lengthToggle', 'value'),
               Input('ageToggle', 'value'),
               Input('select-Language', 'value'),
               Input('select-Age-Group', 'value')])
def update_figure(togglePercentage, selected_genre, selected_years, selected_length, selected_rating, toggle_rating, toggle_length, toggle_age, selected_language, selected_age):
    filtered_df1 = df1
    NetflixTotal = safeFilterCounts(filtered_df1, "Netflix")
    HuluTotal = safeFilterCounts(filtered_df1, "Hulu")
    PrimeTotal = safeFilterCounts(filtered_df1, "Prime Video")
    DisneyTotal = safeFilterCounts(filtered_df1, "Disney+")


    print(selected_genre)
    print(selected_years)
    print(selected_length)
    print(selected_rating)
    print(selected_language)
    if selected_genre:
        if "All" not in selected_genre:
            global globalGenre
            globalGenre = selected_genre
            for genre in selected_genre:
                filtered_df1 = filtered_df1[filtered_df1["Genres"].str.contains(genre, na=False)]

    if selected_language:
        if "All" not in selected_language:
            global globalLanguage
            globalLanguage = selected_language
            for language in selected_language:
                filtered_df1 = filtered_df1[filtered_df1["Language"].str.contains(language, na=False)]

    if selected_age:
        if "All" not in selected_age:
            global globalAgeGroup
            globalAgeGroup = selected_age
            for age in selected_age:
                filtered_df1 = filtered_df1[filtered_df1["Age"].str.contains(age, na=False)]

    if toggle_age:
        global globalYearBool
        globalYearBool = True
        if selected_years:
            global globalYears
            globalYears = [selected_years[0], selected_years[1]]
            filtered_df1 = filtered_df1[
                (selected_years[0] <= filtered_df1["Year"]) & (filtered_df1["Year"] <= selected_years[1])]

    if toggle_length:
        global globalLengthBool
        globalLengthBool = True
        if selected_length:
            global globalLengths
            globalLengths = [selected_length[0], selected_length[1]]
            filtered_df1 = filtered_df1[
                (filtered_df1["Runtime"].notna())]
            filtered_df1 = filtered_df1[
                ((selected_length[0] <= filtered_df1["Runtime"]) & (filtered_df1["Runtime"] <= selected_length[1]))]

    if toggle_rating:
        global globalRatingBool
        globalRatingBool = True
        if selected_rating:
            global globalRating
            globalRating = selected_rating
            filtered_df1 = filtered_df1[
                    (filtered_df1["Rotten Tomatoes"].notna())]
            filtered_df1 = filtered_df1[(selected_rating <= filtered_df1["Rotten Tomatoes"].str.rstrip("%").astype(int))]

    new_df1 = safeFilterCounts(filtered_df1, "Netflix")
    new_df2 = safeFilterCounts(filtered_df1, "Hulu")
    new_df3 = safeFilterCounts(filtered_df1, "Prime Video")
    new_df4 = safeFilterCounts(filtered_df1, "Disney+")
    if togglePercentage:
        new_df1 = round((new_df1 / NetflixTotal), 2) * 100
        new_df2 = round((new_df2 / HuluTotal), 2) * 100
        new_df3 = round((new_df3 / PrimeTotal), 2) * 100
        new_df4 = round((new_df4 / DisneyTotal), 2) * 100
        data_interactive_barchart = [
            go.Bar(x=['Netflix', 'Hulu', 'Prime Video', 'Disney+'], y=[new_df1, new_df2, new_df3, new_df4])]
        return {'data': data_interactive_barchart,
                'layout': go.Layout(title='percentage of films on each streaming service matching filter criteria',
                                    xaxis={'title': 'Service'},
                                    yaxis={'title': 'percentage of films'})}

    else:
        data_interactive_barchart = [
            go.Bar(x=['Netflix', 'Hulu', 'Prime Video', 'Disney+'], y=[new_df1, new_df2, new_df3, new_df4])]
        return {'data': data_interactive_barchart,
                'layout': go.Layout(title='Number of movies on each streaming service',
                                    xaxis={'title': 'Service'},
                                    yaxis={'title': 'Number of films'})}

#callback to update the netflix movie list
@app.callback(Output('netflixTable', 'data'),
               Input('listGen', 'value'))
def update_table(genVal):
    filtered_df1 = df1

    if genVal:
        filtered_df1 = filterForBar(filtered_df1)

        netflixData = filtered_df1[filtered_df1['Netflix'] == 1]
        netflixData = netflixData[list(set(df1.columns) - set(["Netflix", "Hulu", "Prime Video", "Disney+"]))].to_dict('records')
        return netflixData

#callback to update the hulu movie list
@app.callback(Output('huluTable', 'data'),
              Input('listGen', 'value'))
def update_table(genVal):
    filtered_df1 = df1

    if genVal:
        filtered_df1 = filterForBar(filtered_df1)

        huluData = filtered_df1[filtered_df1['Hulu'] == 1]
        huluData = huluData[list(set(df1.columns) - set(["Netflix", "Hulu", "Prime Video", "Disney+"]))].to_dict('records')
        return huluData

#callback to update the prime video movie list
@app.callback(Output('primeTable', 'data'),
              Input('listGen', 'value'))
def update_table(genVal):
    primefiltered_df1 = df1.copy()

    if genVal:
        primefiltered_df1 = filterForBar(primefiltered_df1)

        primeData = primefiltered_df1[primefiltered_df1['Prime Video'] == 1]
        primeData = primeData[list(set(df1.columns) - set(["Netflix", "Hulu", "Prime Video", "Disney+"]))].to_dict('records')
        return primeData

#callback to update the disney movie list
@app.callback(Output('disneyTable', 'data'),
              Input('listGen', 'value'))
def update_table(genVal):
    filtered_df1 = df1

    if genVal:
        filtered_df1 = filterForBar(filtered_df1)

        disneyData = filtered_df1[filtered_df1['Disney+'] == 1]
        disneyData = disneyData[list(set(df1.columns) - set(["Netflix", "Hulu", "Prime Video", "Disney+"]))].to_dict('records')
        return disneyData

#function to filter dataframes
def filterForBar(df):
    if "All" not in globalGenre:
        for genre in globalGenre:
            df = df[df["Genres"].str.contains(genre, na=False)]

    if "All" not in globalLanguage:
        for language in globalLanguage:
            df = df[df["Language"].str.contains(language, na=False)]

    if "All" not in globalAgeGroup:
        for age in globalAgeGroup:
            df = df[df["Age"].str.contains(age, na=False)]

    if globalYearBool:
        if globalYears:
            df = df[
                (globalYears[0] <= df["Year"]) & (df["Year"] <= globalYears[1])]

    if globalLengthBool:
        if globalLengths:
            df = df[
                (df["Runtime"].notna())]
            df = df[
                ((globalLengths[0] <= df["Runtime"]) & (
                             df["Runtime"] <= globalLengths[1]))]

    if globalRatingBool:
        if globalRating:
            df = df[
                (df["Rotten Tomatoes"].notna())]
            df = df[
                (globalRating <= df["Rotten Tomatoes"].str.rstrip("%").astype(int))]

    return df

def safeFilterCounts(dataframe, service):
    try:
        filtered_df = dataframe[service].value_counts()[1]
    except KeyError:
        filtered_df = 0
    return filtered_df

#callback to change pages
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/netList':
        return netflixBarList
    elif pathname == '/huList':
        return huluBarList
    elif pathname == '/pvList':
        return primeBarList
    elif pathname == '/disList':
        return disneyBarList
    elif pathname == '/mainPage':
        #set globals to initial values when initial page is loaded
        global globalGenre
        globalGenre = ["All"]

        global globalRatingBool
        globalRatingBool = False

        global globalRating
        globalRating = 0
        global globalLengthBool
        globalLengthBool = False

        global globalLengths
        globalLengths = [0, 1256]

        global globalYearBool
        globalYearBool = False
        global globalYears
        globalYears = None

        global globalLanguage
        globalLanguage = ["All"]

        global globalAgeGroup
        globalAgeGroup = ["All"]

        return page_1_layout
    else:
        return home_page

if __name__ == '__main__':
    app.run_server()





for epoch in range(num_epochs):
    for n, (real_samples, _) in enumerate(train_loader):
        
        # Data for training the discriminator
        real_samples_labels = torch.ones((batch_size, 1))
        latent_space_samples = torch.randn((batch_size, 2))
        generated_samples = generator(latent_space_samples)
        generated_samples_labels = torch.zeros((batch_size, 1))
        all_samples = torch.cat((real_samples, generated_samples))
        all_samples_labels = torch.cat((real_samples_labels, generated_samples_labels))
        
        # Training the discriminator
        discriminator.zero_grad()
        output_discriminator = discriminator(all_samples)
        loss_discriminator = loss_function(output_discriminator, all_samples_labels)
        loss_discriminator.backward()
        optimizer_discriminator.step()
        
        # Data for training the generator
        latent_space_samples = torch.rand((batch_size, 2))
        
        # Training the generator
        generator.zero_grad()
        generated_samples = generator(latent_space_samples)
        output_discriminator_generated = discriminator(generated_samples)
        loss_generator = loss_function(output_discriminator_generated, real_samples_labels)
        loss_generator.backward()
        optimizer_generator.step()
        
        # show loss
        if epoch % 10 == 0 and n == batch_size - 1:
            print(f"Epoch: {epoch} Loss Discrim.: {loss_discriminator}")
            print(f"Epoch: {epoch} Loss Gen: {loss_generator}")