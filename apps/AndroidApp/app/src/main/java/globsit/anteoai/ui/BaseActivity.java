package globsit.anteoai.ui;

import android.app.DownloadManager;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.net.http.SslError;
import android.os.Bundle;
import android.os.Environment;
import android.text.TextUtils;
import android.util.Log;
import android.webkit.CookieManager;
import android.webkit.DownloadListener;
import android.webkit.SslErrorHandler;
import android.webkit.URLUtil;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import globsit.anteoai.R;
import globsit.anteoai.utils.NetworkCheck;
import globsit.anteoai.utils.PreferencesManager;

public class BaseActivity extends AppCompatActivity {

    public static final String USER_AGENT_FAKE = "GSSC";
    protected NetworkCheck mNetworkCheck;
    protected PreferencesManager mPreferencesManager;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mNetworkCheck = new NetworkCheck(this);
        mPreferencesManager = new PreferencesManager(this);
    }
    
    protected void setUpWebview(WebView webview){
        webview.getSettings().setBuiltInZoomControls(false);
        webview.getSettings().setCacheMode(WebSettings.LOAD_DEFAULT);
        webview.getSettings().setDomStorageEnabled(true);
        webview.getSettings().setJavaScriptEnabled(true);
        webview.getSettings().setJavaScriptCanOpenWindowsAutomatically(true);
        webview.getSettings().setSupportZoom(true);
        webview.getSettings().setUseWideViewPort(false);
        webview.getSettings().setLoadWithOverviewMode(false);
        webview.getSettings().setUserAgentString(USER_AGENT_FAKE);

        webview.setWebViewClient(new WebViewClient() {

            @Override
            public void onReceivedSslError(WebView view,
                                           final SslErrorHandler handler, SslError error) {
                try {
                    final AlertDialog.Builder builder = new AlertDialog.Builder(BaseActivity.this);
                    builder.setMessage(R.string.notification_error_ssl_cert_invalid);
                    builder.setPositiveButton("continue", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            handler.proceed();
                        }
                    });
                    builder.setNegativeButton("cancel", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            handler.cancel();
                        }
                    });
                    final AlertDialog dialog = builder.create();
                    dialog.show();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                super.onReceivedError(view, request, error);
                Log.i("error",error.getDescription().toString());
                //Toast.makeText(BaseActivity.this,"received error",Toast.LENGTH_SHORT).show();
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                Log.i("url",url);
                if((url.contains("anteo.ai") && (! url.contains("referer=")))) {
                    if (url.endsWith(".pdf") /*|| url.startsWith("https://anteo.ai/reports/")*/){
                        /*String pdfUrl = "https://docs.google.com/viewer?url=" + url;
                        view.loadUrl(pdfUrl);*/
                        Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                        view.getContext().startActivity(i);
                    } else {
                        view.loadUrl(url);
                    }
                } else {
                    Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                    view.getContext().startActivity(i);
                    return true;
                }
                if(!mNetworkCheck.connectivityCheck()){
                    setNetworkStatus(false);
                    return true;
                }else{
                    return false;
                }
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                /*if(url.equalsIgnoreCase(*//*"http://port-80.democontainer-fierro905117.codeanyapp.com/logout"*//*"https://gssc.globsit.com/logout")){
                    CookieManager.getInstance().removeAllCookies(null);
                    webview.clearCache(true);
                }else{*/
                    CookieManager.getInstance().setAcceptCookie(true);
                    CookieManager.getInstance().setAcceptThirdPartyCookies(webview,true);
                    CookieManager.getInstance().flush();
                //}
            }
        });

        webview.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                super.onProgressChanged(view, newProgress);
                setLoadingProgress(newProgress);
            }
        });

        webview.setDownloadListener(new DownloadListener()
        {
            @Override
            public void onDownloadStart(String url, String userAgent,
                                        String contentDisposition, String mimeType,
                                        long contentLength) {
                if(url.startsWith("https://anteo.ai/reports/")){
                    DownloadManager.Request request = new DownloadManager.Request(
                            Uri.parse(url));
                    request.setMimeType(mimeType);
                    String cookies = CookieManager.getInstance().getCookie(url);
                    request.addRequestHeader("cookie", cookies);
                    request.addRequestHeader("User-Agent", userAgent);
                    request.setDescription("Downloading File...");
                    request.setTitle(URLUtil.guessFileName(url, contentDisposition, mimeType));
                    request.allowScanningByMediaScanner();
                    request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
                    request.setDestinationInExternalPublicDir(
                            Environment.DIRECTORY_DOWNLOADS, URLUtil.guessFileName(
                                    url, contentDisposition, mimeType));
                    DownloadManager dm = (DownloadManager) getSystemService(DOWNLOAD_SERVICE);
                    dm.enqueue(request);
                    Toast.makeText(getApplicationContext(), "Downloading File", Toast.LENGTH_LONG).show();
                }
            }});

    }

    protected void setNetworkStatus(boolean status){

    }

    protected void setLoadingProgress(int progress){

    }

    protected void loadOrRefreshUrl(WebView webview,String url) {
        if (mNetworkCheck.connectivityCheck()) {
            setNetworkStatus(true);
            if (TextUtils.isEmpty(webview.getUrl()))
                webview.loadUrl(url);
            else
                webview.reload();
        } else
            setNetworkStatus(false);
    }
}
