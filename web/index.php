<html>
    <?php
        $host_name = 'db739889303.db.1and1.com';
        $database = 'db739889303';
        $user_name = 'dbo739889303';
        $password = 'cga8aJsEuawrvwbU04TY!';

        $connect = mysql_connect($host_name, $user_name, $password, $database);
        if (mysql_errno()) {
            die('<p>Failed to connect to MySQL: '.mysql_error().'</p>');
        } else {
            echo '<p>Connection to MySQL server successfully established.</p >';
        }
    ?>
</html>