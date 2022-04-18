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
<html>
	<head>
		<title>ING Robotics Aviation: OMEN ESC MONITOR</title>
		<!--<meta http-equiv="refresh" content="<?php echo $sec?>;URL='<?php echo $page?>'">-->
			<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
			<script>
				$(document).ready(function(){
					setInterval(function(){
						$("#autodata1").load("esc1.php");
						refresh();
					}, 5);
				});
				
				$(document).ready(function(){
					setInterval(function(){
						$("#autodata2").load("esc2.php");
						refresh();
					}, 5);
				});
				
				$(document).ready(function(){
					setInterval(function(){
						$("#autodata3").load("esc3.php");
						refresh();
					}, 5);
				});
				
				$(document).ready(function(){
					setInterval(function(){
						$("#autodata4").load("esc4.php");
						refresh();
					}, 5);
				});
				
				$(document).ready(function(){
					setInterval(function(){
						$("#autodata5").load("esc5.php");
						refresh();
					}, 5);
				});
				
				$(document).ready(function(){
					setInterval(function(){
						$("#autodata6").load("esc6.php");
						refresh();
					}, 5);
				});
				
				$(document).ready(function(){
					setInterval(function(){
						$("#autodata7").load("esc7.php");
						refresh();
					}, 5);
				});
				
				$(document).ready(function(){
					setInterval(function(){
						$("#autodata8").load("esc8.php");
						refresh();
					}, 5);
				});
			</script>
		<style>
				body {
					width: 100%;
					margin: 0 auto;
					font-family: Tahoma, Verdana, Arial, sans-serif;
					text-align:center;
				}
				.angles {
					width:100%;
					height:10%;
					border:1px solid #C0C0C0;
					border-collapse:collapse;
					padding:5px;
				}
				.angles th {
					border:1px solid #C0C0C0;
					padding:5px;
					background:#F0F0F0;
				}
				.angles td {
					border:1px solid #C0C0C0;
					text-align:center;
					padding:5px;
					font-size: 300%;
				}
				.LA {
					color:blue;
				}
				.ALT {
					color:red;
				}
				img {
				  max-width: 5%;
				  height: auto;
				}
		</style>
	</head>
	<body>
	<h1>OMEN ESC MONITORING </h1>
	<br><hr><br>
	<h2> ESC 1 - Status </h2>
		<center id="autodata1">
			<?php
			include 'esc1.php';
			?>
		</center>
	<hr>
	<h2> ESC 2 - Status </h2>
		<center id="autodata2">
			<?php
			include 'esc2.php';
			?>
		</center>
	<hr>	
	<h2> ESC 3 - Status </h2>
		<center id="autodata3">
			<?php
			include 'esc3.php';
			?>
		</center>
	<hr>
	<h2> ESC 4 - Status </h2>
		<center id="autodata4">
			<?php
			include 'esc4.php';
			?>
		</center>
	<hr>
	<h2> ESC 5 - Status </h2>
		<center id="autodata5">
			<?php
			include 'esc5.php';
			?>
		</center>
	<hr>
	<h2> ESC 6 - Status </h2>
		<center id="autodata6">
			<?php
			include 'esc6.php';
			?>
		</center>
	<hr>
	<h2> ESC 7 - Status </h2>
		<center id="autodata7">
			<?php
			include 'esc7.php';
			?>
		</center>
	<hr>
	<h2> ESC 8 - Status </h2>
		<center id="autodata8">
			<?php
			include 'esc8.php';
			?>
		</center>
	<hr>
	</body>
	
		<script>
		  $(function() {
			$('#table').bootstrapTable()
		  })
		</script>
</html>