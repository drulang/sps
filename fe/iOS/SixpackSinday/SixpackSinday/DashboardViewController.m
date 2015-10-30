//
//  DashboardViewController.m
//  SixpackSinday
//
//  Created by Dru Lang on 4/8/14.
//  Copyright (c) 2014 drulang. All rights reserved.
//

#import "DashboardViewController.h"

@interface DashboardViewController ()
@property (weak, nonatomic) IBOutlet UILabel *welcomeLabel;

@end

@implementation DashboardViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    //NSString *un = self.user.username;
    self.welcomeLabel.text = [NSString stringWithFormat:@"Welcome, %@", self.user.username];
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
