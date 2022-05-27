package globsit.anteoai.ui;

import androidx.databinding.DataBindingUtil;

import android.os.Bundle;
import android.view.View;

import globsit.anteoai.R;
import globsit.anteoai.databinding.ActivityHomeBinding;

public class HomeActivity extends BaseActivity {

    private ActivityHomeBinding mBinding;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mBinding = DataBindingUtil.setContentView(this, R.layout.activity_home);
        setUpWebview(mBinding.webview);
        loadOrRefreshUrl(mBinding.webview,getString(R.string.web_url));
    }

    public void onMenuItemClick(View view) {
       if (view.getId() == R.id.fab_refresh) {
            loadOrRefreshUrl(mBinding.webview,getString(R.string.web_url));
       }
    }

    @Override
    protected void setNetworkStatus(boolean status) {
        super.setNetworkStatus(status);
        mBinding.setNetwork(status);
    }

    @Override
    protected void setLoadingProgress(int progress) {
        super.setLoadingProgress(progress);
        mBinding.setProgress(progress);
    }
}