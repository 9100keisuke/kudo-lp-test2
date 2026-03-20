/**
 * Google Apps Script — LP ABテスト用フォーム受信エンドポイント
 *
 * 使い方:
 * 1. Google Sheetsで「LP-ABテスト」シートを作成
 * 2. Apps Script エディタにこのコードを貼り付け
 * 3. ウェブアプリとしてデプロイ（アクセス: 全員）
 * 4. デプロイURLをLP内のFORM_ENDPOINTに設定
 */

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // ヘッダーが無ければ追加
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['timestamp', 'email', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'pattern']);
    }

    sheet.appendRow([
      new Date().toISOString(),
      data.email || '',
      data.utm_source || 'direct',
      data.utm_medium || 'none',
      data.utm_campaign || 'none',
      data.utm_content || '',
      data.pattern || ''
    ]);

    return ContentService.createTextOutput(JSON.stringify({status: 'ok'}))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({status: 'error', message: err.message}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput('LP ABテスト endpoint is running')
    .setMimeType(ContentService.MimeType.TEXT);
}
