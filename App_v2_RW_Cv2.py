#!/usr/bin/env python
# coding: utf-8
import time
import asyncio
# In[5]:

import panel as pn

import pandas as pd
from io import StringIO
from PIL import Image
import numpy as np
from bokeh.plotting import figure, output_file, show, Column
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource

pn.extension()


# ###  Aque d'aix side  front

# In[36]:


# text input to get xinit and ynit values
X = pn.widgets.TextInput(name='Xinit', value='Xinit value', width=170)
Y = pn.widgets.TextInput(name='Yinit', value='Yinit value', width=170)

# bottons for tracing path and getting xinit, yinit

# Side front of the first method
sideWidgets = pn.Column((pn.Column()), pn.Row(X, Y), margin=(20, 5, 5, 5))
sideFrontwidgets = pn.Tabs(('Parameters', sideWidgets))

# side front
sideFront = pn.Column(background='#F6F6F6')

# In[37]:


html_pane = pn.pane.HTML("""

  <h2  style="font-size:25px; color: #0072AB; font-family: Display"; > 
  <img src=https://www.fetedelascience.fr/sites/default/files/styles/homepage_logo/public/2022-04/Logo-CEREGE_7.png?itok=1M8GH37_ 
  width="100" height="100">
  Counting laminates of varved carbonated concretions Application </h2>

<p style="line-height : 25px"> This application is developed for the purpose of counting
laminates of varved carbonated concretions using image processing. </p>
<br>
<p> To use this application, you will need to : </p>
<br>
<ol style="line-height : 30px">
  <li>  Select your folder directory from the file selector </li>
  <li > Choose the image you want to work with and pass it to <br> the selected files </li>
  <li> Click the load buttton to load your imageTab </li>
  <li> Click the method of processing you want to use </li>
</ol

""", style={'border-radius': '5px', 'padding': '10px'}, width=400)

# ### Aque d'aix main front

# In[38]:


# file input to load the image
FileInput = pn.widgets.FileSelector('~')  # exucuting button to exucute the application

Figure = pn.Column()
figurePath = pn.Column()
imageTab = pn.Tabs(margin=(20, 5, 5, 5), closable=True)

getButtons = pn.Column()
# making the main layout

mainFront = pn.Column()


# In[39]:


# Main front of the first page


# In[40]:


def main_image():
    buttonGetXY = pn.widgets.Button(name='Get XY init and trace the path', button_type='primary', width=250)
    sideWidgets[0] = buttonGetXY
    im = Image.open(FileInput.value[0])  # just replace any image that you want her
    imarray = np.flipud(np.array(im.convert("RGBA")))
    p = figure(x_range=(0, imarray.shape[1]), y_range=(0, imarray.shape[0]))
    p.image_rgba(image=[imarray.view("uint32").reshape(imarray.shape[:2])], x=0, y=0, dw=imarray.shape[1],
                 dh=imarray.shape[0])

    '''   im = Image.open(FileInput.value[0]).convert('RGBA') # just replace any image that you want her


    imarray = np.flipud(np.asarray(im))

    #p = figure()
    #p.image_rgba(image=[imarray.view("uint32").reshape(imarray.shape[:2])], x=0, y=0, dw=imarray.shape[0],
                 #dh=imarray.shape[1])


    # Open image, and make sure it's RGB*A*

    xdim, ydim = im.size

    img = np.empty((ydim, xdim), dtype=np.uint32)
    view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))

    view[:,:,:] = np.flipud(np.asarray(im))
    # Display the 32-bit RGBA image
    dim = max(xdim, ydim)
    p = figure(x_range=(0,dim), y_range=(0,dim))
    p.image_rgba(image=[img], x=0, y=0, dw=ydim, dh=xdim)'''

    # creating an empty list to have a 0 point in the beginning
    source = ColumnDataSource({'x': [], 'y': [], 'color': []})
    renderer = p.scatter(x='x', y='y', source=source, color='red', size=10)

    draw_tool = PointDrawTool(renderers=[renderer], empty_value='black', num_objects=1)
    p.add_tools(draw_tool)
    p.toolbar.active_tap = draw_tool
    Figure.append(p)
    imageTab.append(('imageTab', Figure))

    def get_xy(event):
        if len(source.data['x']) == 0 and len(source.data['y']) == 0:
            pass
        else:
            p = figure(x_range=(0, imarray.shape[1]), y_range=(0, imarray.shape[0]))
            p.image_rgba(image=[imarray.view("uint32").reshape(imarray.shape[:2])], x=0, y=0, dw=imarray.shape[1],
                         dh=imarray.shape[0])
            x = round(source.data['x'][0])
            y = round(source.data['y'][0])
            X.value = '{0}'.format(imarray[y][x])
            Y.value = '{0}'.format(source.data['y'][0])

            path = {'x': [source.data['x'][0]], 'y': [source.data['y'][0]], 'color': ['red']}

            dataSourceTable = ColumnDataSource(data=path)
            p.line(x='x', y='y', source=dataSourceTable, line_width=2)
            p.circle(x='x', y='y', source=dataSourceTable, fill_color="white", size=8)
            columns = [TableColumn(field="x", title="x"),
                       TableColumn(field="y", title="y"),
                       TableColumn(field="color", title="color")]
            table = DataTable(source=dataSourceTable, columns=columns, editable=True)

            buttonStart = pn.widgets.Button(name='► Start', button_type='primary', width=100)
            get_table_column = pn.Row(buttonStart, margin=(5, 5, 5, 5))

            def update():
                #if len(dataSourceTable.data['x']) < 10 and len(dataSourceTable.data['y']) < 10:
                    def generate_random():
                        x = dataSourceTable.data['x'][(len(dataSourceTable.data['x']) - 1)]
                        y = dataSourceTable.data['y'][(len(dataSourceTable.data['y']) - 1)]
                        step = np.random.uniform(0, 1)
                        if step < 0.5:
                            x += np.random.uniform(10, 20)
                            y -= 20
                        if step > 0.5:
                            x -= np.random.uniform(10, 20)
                            y -= 20
                        return x, y

                    x, y = generate_random()
                    if ((imarray[round(y)][round(x)] == [0, 0, 0, 255]).all()):
                        new_data = {
                            'x': [x],
                            'y': [y],
                            'color': ['red']
                        }
                        dataSourceTable.stream(new_data)
                    else:
                        x, y = generate_random()


                #else:
                    #buttonStart.name = 'Download Table'
                    #buttonStart.button_type = 'success'

            callback = pn.state.add_periodic_callback(update, 200, start=False)

            def randomwalk(event):
                if buttonStart.name == '► Start':
                    buttonStart.name = '❚❚ Pause'
                    callback.start()
                elif buttonStart.name == '❚❚ Pause':
                    buttonStart.name = '► Start'
                    callback.stop()
                else:
                    df = {'x': [], 'y': []}
                    fileToDownload = StringIO()
                    df = dataSourceTable.data
                    pd.DataFrame(path).to_csv(fileToDownload, index=True, sep='\t')
                    fileToDownload.seek(0)
                    fd = pn.widgets.FileDownload(fileToDownload, embed=True, filename='Table_Data.csv', width=170)
                    if len(get_table_column) == 1:
                        get_table_column.append(fd)
                    else:
                        get_table_column.remove(get_table_column[1])
                        get_table_column.append(fd)

            buttonStart.on_click(randomwalk)
            if len(imageTab) == 1:
                imageTab.append(('path', pn.Column(get_table_column, pn.Row(p, table))))
            else:
                imageTab.remove(imageTab[1])
                imageTab.append(('path', pn.Column(get_table_column, pn.Row(p, table))))

    buttonGetXY.on_click(get_xy)


def load_app():
    buttonLoadImage = pn.widgets.Button(name='Load', button_type='primary', width=50)
    fileInputLodButton = pn.Row(FileInput, buttonLoadImage)
    mainWidgets = pn.Column(fileInputLodButton)
    mainFront.append(mainWidgets)
    mainFront.append(imageTab)
    X.value = 'Xinit value'
    Y.value = 'Yinit value'
    sideFront.append(html_pane)
    buttonMethod1 = pn.widgets.Button(name='First method', button_type='primary', width=150)
    buttonMethod2 = pn.widgets.Button(name='Second method', button_type='primary', width=150)
    sideRow = pn.Row(buttonMethod1, buttonMethod2)
    sideFront.append(sideRow)

    def click_button_load_image(event):
        if len(FileInput.value) == 0:
            pass
        else:
            main_image()

            def method_1(event):
                sideFront.clear()
                sideFront.append(sideFrontwidgets)

            buttonMethod1.on_click(method_1)

            buttonReset = pn.widgets.Button(name='Reset', button_type='warning')
            buttonMainRow = pn.Row(buttonReset)
            mainWidgets[0] = buttonMainRow

            def reset(event):
                sideFront.clear()
                Figure.clear()
                imageTab.clear()
                mainFront.clear()
                load_app()

            buttonReset.on_click(reset)

    buttonLoadImage.on_click(click_button_load_image)


load_app()

# ### lanching Aque d'aix

# In[41]:


ACCENT_COLOR = "#0072AB"
aqueDAix = pn.template.VanillaTemplate(site="Panel", title="Aque d'Aix", sidebar_width=400,
                                       accent_base_color=ACCENT_COLOR, header_background=ACCENT_COLOR)
aqueDAix.main.append(mainFront)
aqueDAix.sidebar.append(sideFront)
aqueDAix.show()
