<h1>Pet Feeder Backend</h1>
<h2>List Of Contents</h2>
<ul>
    <li><h3><a href="#Setup">Setup</a></h3></li>
    <li><h3><a href="#Database">Data Base Model</a></h3></li>
        <ul>
            <li><a href="#D-Pet">Pet</a></li>
            <li><a href="#D-Food">Food</a></li>
            <li><a href="#D-Meal">Meal</a></li>
        </ul>
    <li><h3><a href="#API-Endpoints">Rest API</a></h3></li>
        <ul>
            <li><a>Endpoints</a></li>
        </ul>
</ul>
<hr>
<h2 id="Setup">Setting up Django Project</h2>

<ol>
  <li>
    <strong>Navigate to the project directory</strong>
    <pre><code>cd this-repo</code></pre>
    <p>Replace <code>this-repo</code> with your actual directory name.</p>
  </li>
  <li>
    <strong>Create a virtual environment</strong>
    <p>Creating a virtual environment is recommended as it isolates your Python/Django setup on a per-project basis.</p>
    <pre><code>python -m venv env</code></pre>
    <p>This will create a new virtual environment in the <code>env</code> directory.</p>
  </li>
  <li>
    <strong>Activate the virtual environment</strong>
    <p>If you're on a Windows machine:</p>
    <pre><code>env\Scripts\activate</code></pre>
    <p>If you're on Unix or MacOS:</p>
    <pre><code>source env/bin/activate</code></pre>
  </li>
  <li>
    <strong>Install dependencies</strong>
    <p>Here, we'll use pip to install Django and other dependencies from the <code>requirements.txt</code>file:</p>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>
    <strong>Migrate the database</strong>
    <p>Django comes with built-in commands for migrating your database. Here's how you do it:</p>
    <pre><code>python manage.py makemigrations
python manage.py migrate</code></pre>
  </li>
  <li>
    <strong>Create a superuser</strong>
    <p>This command will allow you to create an admin user (superuser) who can log into the Django admin site:</p>
    <pre><code>python manage.py createsuperuser</code></pre>
    <p>You'll be asked to enter an email address and a password for the superuser.</p>
  </li>
  <li>
    <strong>Run the Django app</strong>
    <p>Use the following command to start the server:</p>
    <pre><code>python manage.py runserver</code></pre>
    <p>You should now be able to access your Django project at <a href="http://127.0.0.1:8000"><code>http://127.0.0.1:8000</code></a>.</p>
  </li>
</ol>

<p>This setup guide assumes Python and Pip are already installed on the machine. It's also important to note that the
default server setup is sufficient for development purposes. 
When running in a production scenario, consider using an actual server like Gunicorn or uWSGI.</p>

<hr>
<h2 id="Database">Database Documentation</h2>
<img src="Meal_Diagramm.png" width=400>
<p>Our database is made up of three tables: <code>Pet</code>, <code>Food</code>, and <code>Meal</code>.</p>

<h3 id="D-Pet">1. Pet</h3>

<p>This table stores all data related to pets. Here are the fields for <code>Pet</code>:</p>

<ul>
  <li><code>name</code>: A <code>CharField</code> storing the name of the pet. Maximum length is 30 characters.</li>
  <li><code>age</code>: An <code>IntegerField</code> storing the age of the pet.</li>
  <li><code>race</code>: A <code>CharField</code> storing the race of the pet. Maximum length is 40 characters.</li>
</ul>

<p>This model returns the <code>name</code> field in its <code>__str__</code> method. The pets are ordered by their <code>name</code> in ascending order.</p>

<h3 id="D-Food">2. Food</h3>

<p>This table stores all data related to pet food. Here are the fields for <code>Food</code>:</p>

<ul>
  <li><code>name</code>: A <code>CharField</code> storing the name of the food. Maximum length is 100 characters.</li>
  <li><code>brand</code>: A <code>CharField</code> storing the brand of the food. Maximum length is 30 characters.</li>
  <li><code>category</code>: A <code>CharField</code> storing the category to which the food belongs. It can be 'Dry' (D), 'Wet' (W), or 'Snack' (S). Its length is set to 1 character.</li>
  <li><code>price</code>: An <code>IntegerField</code> storing the price of the food.</li>
  <li><code>unit</code>: A <code>CharField</code> indicating in which unit the food is measured. It can be 'grams' (g) or 'milliliters' (ml). Its length is set to 1 character.</li>
</ul>

<h3 id="D-Meal">3. Meal</h3>

<p>This table stores all data related to the meals the pets have. Here are the fields for <code>Meal</code>:</p>

<ul>
  <li><code>time</code>: A <code>DateTimeField</code> storing the timestamp when the meal was created. It is automatically set to the time of creation.</li>
  <li><code>food</code>: A <code>ForeignKey</code> linking to the <code>Food</code> model. If the food instance is deleted, all meals associated with it will also be deleted due to the <code>CASCADE</code> deletion rule.</li>
  <li><code>pet</code>: A <code>ForeignKey</code> linking to the <code>Pet</code> model. If the pet instance is deleted, all meals associated with it will also be deleted due to the <code>CASCADE</code> deletion rule.</li>
  <li><code>quantity</code>: An <code>IntegerField</code> storing the quantity of food consumed during the meal. Its default value is 0.</li>
</ul>

<p>These models should altogether provide a comprehensive overview of pet meals, including what foods are eaten, by which pets, and in what quantities.</p>

<hr>
<h2>Rest API Documentation</h2>
<h3>Running the Server</h3>

<p>To start your Django server, first, ensure you're in the directory that contains the <code>manage.py</code>
file.
Use the command line to navigate to this directory,
then run the following command: <code>python manage.py runserver</code>
The system will start a development server, typically accessible at 
<a href="http://127.0.0.1:8000/"><code>http://127.0.0.1:8000/</code></a> .
</p>
<h3>Examining the API</h3>

<p>When the Django server is on and active, you are able to view your API by accessing <a href="http://127.0.0.1:8000/"><code>http://127.0.0.1:8000/</code></a> from your browser of choice. Ensuring that your Django Rest Framework's navigable API feature is switched on, you will be able to browse through the API conveniently from your browser itself.</p>

<p>To get to the specific endpoints as previously detailed in the API documentation, simply add your desired endpoint to the base URL. 
For example, if you aim to view and create meals, you would access 
<a href="http://127.0.0.1:8000/meals/"><code>http://127.0.0.1:8000/meals/</code></a>.</p>
<h3>Meal Endpoints</h3>

<h4>List and Create Meals</h4>
<ul>
  <li>Endpoint: <code>/meals/</code></li>
  <li>Method: <code>GET, POST</code></li>
</ul>

<h4>Retrieve, Update and Delete a Specific Meal</h4>
<ul>
  <li>Endpoint: <code>/meals/&lt;id&gt;/</code></li>
  <li>Method: <code>GET, PUT, PATCH, DELETE</code></li>
</ul>

<h4>Get Daily Meals</h4>
<ul>
  <li>Endpoint: <code>/meals/daily_meals/</code></li>
  <li>Method: <code>GET</code></li>
</ul>

<h3>Food Endpoints</h3>

<h4>List and Create Foods</h4>
<ul>
  <li>Endpoint: <code>/foods/</code></li>
  <li>Method: <code>GET, POST</code></li>
</ul>

<h4>Retrieve, Update and Delete a Specific Food</h4>
<ul>
  <li>Endpoint: <code>/foods/&lt;id&gt;/</code></li>
  <li>Method: <code>GET, PUT, PATCH, DELETE</code></li>
</ul>

<h3>Pet Endpoints</h3>

<h4>List and Create Pets</h4>
<ul>
  <li>Endpoint: <code>/pets/</code></li>
  <li>Method: <code>GET, POST</code></li>
</ul>

<h4>Retrieve, Update and Delete a Specific Pet</h4>
<ul>
  <li>Endpoint: <code>/pets/&lt;id&gt;/</code></li>
  <li>Method: <code>GET, PUT, PATCH, DELETE</code></li>
</ul>


