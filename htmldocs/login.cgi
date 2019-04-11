<html xmlns:axsl="http://localhost" lang="fr">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <style type="text/css"></style>
    <meta http-equiv="Content-Script-Type" content="text/javascript">
    <meta http-equiv="Cache-Control" content="no-cache">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="-1">
    <script language="JavaScript" src="/scripts/common.js" type="text/javascript"></script>
    <script language="JavaScript" src="/scripts/reload.js" type="text/javascript"></script>
    <script language="JavaScript" src="/scripts/ajax.js" type="text/javascript"></script>
    <link href="/css/common.css" type="text/css" rel="stylesheet">
    <script language="Javascript" type="text/javascript">
		function reloadPage(){
			location.reload();
		}
	</script>
    <script language="JavaScript" type="text/javascript">
		function openTopPage() {
			var location_base=parent.window.location.pathname.split("/fr/");
			location = "".concat(location_base[0]).concat("/fr/websys/webArch/topPage.cgi");
		}
	</script>
    <script language="JavaScript" type="text/javascript">
		function openConfigListPage() {
			var location_base=parent.window.location.pathname.split("/fr/");
			location = "".concat(location_base[0]).concat("/fr/websys/webArch/configList.cgi");
		}
	</script>
    <script language="JavaScript" type="text/javascript">
		function openJobListPage() {
			var location_base=parent.window.location.pathname.split("/fr/");
			location = "".concat(location_base[0]).concat("/fr/websys/webArch/jobList.cgi");
		}
	</script>
    <style type="text/css">
		table.defaultTableButton {
			font-size:12px;
			border-style: solid;
			border-width: 1px;
			border-color: #8D8D8D;
			cursor:pointer;
		}
		table.defaultTableButton td.defaultTableButton {
			padding: 0px 8px 0px 8px;
			vertical-align: middle;
			background-color: #808080;
			background-image: URL(/images/buttonBGwhite.gif);
			background-repeat: repeat-x;
			text-align: center;
			overflow: hidden;
		}
		table.defaultTableButtonSelected {
			font-size:12px;
			border-style: solid;
			border-width: 1px;
			border-color: #8D8D8D;
			cursor:pointer;
		}
		table.defaultTableButtonSelected td.defaultTableButtonSelected {
			padding: 0px 8px 0px 8px;
			vertical-align: middle;
			background-color: #F7EEB2;
			text-align: center;
			overflow: hidden;
		}
		table.defaultTableButton a.defaultTableButton {
			text-decoration: none;
			color: black;
			white-space: nowrap;
		}
		table.defaultTableButtonSelected a.defaultTableButton {
			text-decoration: none;
			color: black;
			white-space: nowrap;
		}
		table.defaultTableButton a.defaultTableCommandButton {
			text-decoration: none;
			font-weight: bold;
			color: black;
			white-space: nowrap;
		}
		table.defaultTableButtonSelected a.defaultTableCommandButton {
			text-decoration: none;
			font-weight: bold;
			color: black;
			white-space: nowrap;
		}
	</style>
    <script language="JavaScript" type="text/javascript">
		function jumpButtonURL() {
		
			location.href = "/web/guest/fr/websys/webArch/mainFrame.cgi";
		
		}
	</script>
    <style type="text/css">
				body.message { background-color: ; }
			</style>
    <link href="/css/common.css" type="text/css" rel="stylesheet">
    <link href="/css/frame.css" type="text/css" rel="stylesheet" media="all">
    <link href="/css/header.css" type="text/css" rel="stylesheet" media="all">
    <link href="/css/cmnParts.css" type="text/css" rel="stylesheet" media="all">
    <style type="text/css"></style>
    <script language="JavaScript" src="/scripts/jquery.1.4.js" type="text/javascript"></script>
    <script language="JavaScript" src="/scripts/jquery.ui.core.1.4.js" type="text/javascript"></script>
    <script language="JavaScript" src="/scripts/jquery.ui.widget.1.4.js" type="text/javascript"></script>
    <script language="JavaScript" src="/scripts/jquery.ui.mouse.1.4.js" type="text/javascript"></script>
    <script language="JavaScript" src="/scripts/jquery.ui.draggable.1.4.js" type="text/javascript"></script>
    <script language="JavaScript" src="/scripts/jquery.ui.droppable.1.4.js" type="text/javascript"></script>
    <script language="javascript" src="/scripts/head_rollover.js" type="text/javascript"></script>
    <script language="JavaScript">
	function changeImage(id, img){
	  document.images[id].src = "/images/" + img;
	}

	function openNewWindow(target, windowName) {
		window.open(target, windowName);
	}

	function openDiaglogWindow(target, windowName, option) {
		var opt="toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=yes".concat(option);
		window.open(target, windowName, opt);
	}
	
	function headerResize()
	{
		var mainWidth = "100%";
		if( 800 > $(window).width() )
		{
			mainWidth= "800px";
		}
		$("#frameHead").width(mainWidth);
	}

	if (!/*@cc_on!@*/false)
	{
	}
	else
	{
		$(document).ready(function()
		{
			headerResize();
			window.onresize = headerResize;
		});
	}
	
</script>
    <title>Erreur de cookie</title>
  </head>
  <body class="errorMessage">
    <div id="frameHead">
      <div id="logoArea">
        <div id="logo">
          <h1><img src="/images/RICOH.gif" width="104" height="30" alt="RICOH" title="RICOH" class="ver-algn-b"></h1>
          <h2 id="modelName" style="z-index:1;">Aficio MP 301</h2>
          <h3 id="tradeName">Web Image Monitor</h3>
        </div>
      </div>
      <div id="rightArea" style="z-index:1000;">
        <div class="headerSlope"><img src="/images/headerSlope.gif" width="140" height="48" alt=""></div>
        <div id="rightAreaBox"></div>
      </div>
    </div>
    <div id="breadCrumb">
      <ul>
        <li>
          <a class="rollover" onclick="&#10;&#9;&#9;&#9;&#9;&#9;&#9;&#9;location.href='/web/guest/fr/websys/webArch/mainFrame.cgi'; return false;&#10;&#9;&#9;&#9;&#9;&#9;&#9;" href="/web/guest/fr/websys/webArch/topPage.cgi"><img src="/images/headerBtnBack.gif" alt="" name="headerBtnBack" width="4" height="12" id="headerBtnBack" class="mgn-R5px ver-algn-m">Accueil</a>
        </li>
      </ul>
    </div>
    <div style="height:63px;" id="noFrameHeader"></div>
    <a name="link00"></a>
    <table width="100%" height="30" border="0" cellpadding="0" cellspacing="0">
      <tr>
        <td></td>
        <td><img src="/images/spacer.gif" width="1" height="4" border="0" alt="" title=""></td>
        <td></td>
      </tr>
      <tr>
        <td align="left" valign="top" width="12"><img width="12" border="0" src="/images/spacer.gif" alt="" title=""></td>
        <td nowrap width="100%" align="left" height="30">
          <table border="0" cellspacing="0" height="30" width="100%">
            <tr>
              <td nowrap align="left" valign="middle" width="30%">
                <div style="color:black; font-size:16px; font-weight:bold;"><img src="/images/spacer.gif" width="8" height="1" border="0" alt="" title="">Erreur de cookie</div>
              </td>
              <td></td>
              <td width="5"></td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td></td>
        <td>
          <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background:url(/images/settingFlatContsDivision.gif) repeat-x bottom;">
            <tr>
              <td><img src="/images/settingFlatContsDivision.gif" alt="" title=""></td>
            </tr>
          </table>
        </td>
        <td></td>
      </tr>
      <tr>
        <td height="15px"> </td>
      </tr>
    </table>
    <table width="100%" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td nowrap width="12" align="left" valign="top"><img src="/images/spacer.gif" alt="" width="12" height="1" border="0" title=""></td>
        <td align="left" valign="top">
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr class="staticProp">
              <td nowrap width="12" align="left" valign="middle"><img src="/images/messageIconE.gif" alt="" border="0" title=""></td>
              <td><img src="/images/spacer.gif" alt="" width="8" height="1" border="0" title=""></td>
              <td nowrap width="100%" align="left" valign="middle">Erreur</td>
            </tr>
            <tr>
              <td><img src="/images/spacer.gif" alt="" width="1" height="4" border="0" title=""></td>
            </tr>
            <tr class="staticProp">
              <td></td>
              <td></td>
              <td nowrap align="left" valign="top">
                <table border="0" cellspacing="0" cellpadding="0">
                  <tr class="responseMessage">
                    <td align="left" valign="top">Activer les cookies dans le navigateur.</td>
                  </tr>
                  <tr>
                    <td height="8"></td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td height="16"></td>
            </tr>
          </table>
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td>
                <form name="form1">
                  <input type="hidden" name="wimToken" value="1727646085">
                  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background:url(/images/settingDivision.gif) repeat-x bottom;">
                    <tr>
                      <td><img src="/images/settingDivision.gif" alt="" title=""></td>
                    </tr>
                  </table>
                  <table border="0" cellspacing="0" cellpadding="0">
                    <tr class="staticProp">
                      <td>
                        <table border="0" cellspacing="0" cellpadding="0">
                          <tr>
                            <td>
                              <table width="100%" class="defaultTableButton" cellspacing="0">
                                <tr>
                                  <td class="defaultTableButton" onclick="javascript:jumpButtonURL(); return false;" height="20">
                                    <a href="javascript:jumpButtonURL()" class="defaultTableCommandButton">OK</a>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                          <tr>
                            <td nowrap width="1" height="1"><img src="/images/spacer.gif" height="1" width="100" border="0" alt="" title=""></td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table></form>
                <form name="checkForm"></form>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
