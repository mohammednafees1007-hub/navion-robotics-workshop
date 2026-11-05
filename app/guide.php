<?php
$mode=in_array($_GET['mode']??'',['remote','line','obstacle'],true)?$_GET['mode']:'remote';
$steps=guideSteps($mode);$ids=array_column($steps,'id');$index=array_search((string)($_GET['step']??$ids[0]),$ids,true);if($index===false)$index=0;$step=$steps[$index];$meta=$chapterMap[$step['slug']];
$guideUrl=fn($id)=>'?page=guide&mode='.$mode.'&step='.$id;
?>
<p class="eyebrow">BUILD AT YOUR PACE · STEP <?=$index+1?> / <?=count($steps)?></p>
<h1><?=e($step['title'])?></h1>
<form method="get" class="page-tools"><input type="hidden" name="page" value="guide"><label>Robot mode <select name="mode"><option value="remote" <?=$mode==='remote'?'selected':''?>>Laptop remote</option><option value="line" <?=$mode==='line'?'selected':''?>>Line follower</option><option value="obstacle" <?=$mode==='obstacle'?'selected':''?>>Obstacle avoidance</option></select></label><button>Choose mode</button></form>
<aside class="preflight"><div><strong>What you need / power</strong><p><?=e($meta['need'])?></p></div><div><strong>Chapter result</strong><p><?=e($meta['result'])?></p></div></aside>
<?php $sketch=['serial'=>'00_Serial_Test','motor-test'=>'01_Remote_Control','remote'=>'01_Remote_Control','sensors'=>'00_Sensor_Check','line'=>'02_Line_Follower','obstacle'=>'03_Obstacle_Avoidance'][$step['slug']]??null;if($sketch):?><p><a class="button" href="?page=download&amp;file=<?=e($sketch)?>">Download <?=e($sketch)?>.ino</a></p><?php endif ?>
<?php preg_match_all('~<aside class="warning">.*?</aside>~s',$step['context'],$warnings);echo implode('',$warnings[0]); ?>
<article class="content"><?=$step['html']?></article>
<?php if($step['slug']==='serial'):?><aside class="note"><strong>Real IDE screenshot pending</strong><p>Follow the written menu names above. A verified screenshot of the classroom IDE has not been supplied.</p></aside><?php endif ?>
<?php if($step['context']):?><details><summary>Chapter checklist, downloads &amp; explanation</summary><?=$step['context']?></details><?php endif ?>
<p><a href="?page=tools#troubleshooter">Not seeing the expected result?</a> · <a href="?page=lesson&amp;slug=<?=e($step['slug'])?>">Full chapter</a></p>
<nav class="lesson-nav" aria-label="Guided steps"><?php if($index>0):?><a href="<?=e($guideUrl($ids[$index-1]))?>">← Back</a><?php endif ?><?php if(isset($ids[$index+1])):?><a class="button" href="<?=e($guideUrl($ids[$index+1]))?>">Next →</a><?php else:?><a href="?page=downloads">Finish · Save the manual</a><?php endif ?></nav>
<details><summary>Resume any step</summary><ol><?php foreach($steps as $s):?><li><a href="<?=e($guideUrl($s['id']))?>"><?=e($s['title'])?></a></li><?php endforeach ?></ol></details>
<div class="page-tools js-only"><label><input type="checkbox" id="remember-step"> Remember this step on this device</label><button type="button" class="secondary" id="reset-local">Reset saved step &amp; worksheet</button></div><p class="muted">Shared lab computer? Reset before leaving. Saved steps are reading bookmarks, never proof that hardware is safe.</p>
