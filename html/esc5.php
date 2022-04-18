<?php
	$servername = "localhost";
	$username = "mabus";
	$password = "seren1ty";
	$dbname = "ESC_OMEN";

	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);

	// Check connection
	if ($conn->connect_error) {
	  die("Connection failed: " . $conn->connect_error);
	}
	echo "Connected successfully";
?>


<?php

	$result = mysqli_query($conn,"SELECT * FROM ESC5 ORDER BY ID DESC LIMIT 1");

	echo "<table id='table' class='angles'>
	<tr>
	<th>Voltage</th>
	<th>Current</th>
	<th>Temperature</th>
	</tr>";

	while($row = mysqli_fetch_array($result))
	{
	echo "<tr>";
	//echo "<td>" . $row['ID'] . "</td>";
	echo "<td class='LA'>" . $row['VOLT'] . "</td>";
	echo "<td class='LA'>" . $row['AMP'] . "</td>";
	echo "<td>" . $row['TEMP'] . "</td>";
	echo "</tr>";
	}
	echo "</table>";

	mysqli_close($con);
?>